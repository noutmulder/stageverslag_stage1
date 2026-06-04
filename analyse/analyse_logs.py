#!/usr/bin/env python3
"""Analyseer een UP-Studio validatie-sessielog en genereer verslag-figuren.

Gebruik:
    python3 analyse_logs.py <session.log> [outdir]

Leest de regels die de app logt ([CSV], [FRAME], [BT_RTT], [MARKER],
[BASELINE_*], [FRAME_LOG]) en produceert:
  - pos_vs_tijd.(png|pdf)  : Kalman/display vs. gemeten positie over tijd (DV3 + "stabiel")
  - rtt_histogram.(png|pdf): Bluetooth round-trip verdeling + percentielen (DV1)
  - samenvatting.txt       : RTT-percentielen, DV3-smoothness per as, marker-tabel (DV2)

De figuren zijn bewust eenvoudig en print-/verslag-klaar.
"""
import sys, re, os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# ---------- parsing ----------

def parse(path):
    csv=[]      # (t_ms, encoder, kf_pos, kf_vel, display_pos)
    frame=[]    # (t_ms, display_pos, display_spindle, display_swivel)
    rtt=[]      # rtt_ms
    markers=[]  # dict
    frame_log=[]# (state, t_ms)
    baseline=[] # (state, t_ms, encoder)
    for ln in open(path, encoding="utf-8", errors="replace"):
        if ln.startswith("[CSV] "):
            p=ln[6:].strip().split(",")
            if len(p)>=5:
                meas=float(p[5]) if len(p)>=6 else float("nan")   # genorm. meting (nieuw veld)
                csv.append((int(p[0]),int(p[1]),float(p[2]),float(p[3]),float(p[4]),meas))
        elif ln.startswith("[FRAME] "):
            m=re.match(r"\[FRAME\] t=(\d+) display_pos=([\-\d.]+) display_spindle=([\-\d.]+) display_swivel=([\-\d.]+)",ln)
            if m: frame.append((int(m[1]),float(m[2]),float(m[3]),float(m[4])))
        elif ln.startswith("[BT_RTT] "):
            m=re.search(r"rtt_ms=([\-\d.]+)",ln)
            if m: rtt.append(float(m[1]))
        elif ln.startswith("[FRAME_LOG] "):
            m=re.match(r"\[FRAME_LOG\] (\w+) t=(\d+)",ln)
            if m: frame_log.append((m[1],int(m[2])))
        elif ln.startswith("[BASELINE_"):
            m=re.match(r"\[BASELINE_(\w+)\] t=(\d+) encoder=(\d+)",ln)
            if m: baseline.append((m[1],int(m[2]),int(m[3])))
        elif ln.startswith("[MARKER] "):
            d={}
            mlab=re.search(r'label="([^"]*)"',ln)
            d["label"]=mlab[1] if mlab else ""
            for key in ["n","t","encoder","kf_pos","display_pos","fw_pos","total_mm",
                        "display_mm","fw_mm","spindle_kf","spindle_disp","swivel_kf","swivel_disp"]:
                m=re.search(rf"{key}=([\-\d.]+)",ln)
                d[key]=float(m[1]) if m else float("nan")
            mc=re.search(r"compass_yaw=([\-\d.nan]+)",ln)
            d["compass_yaw"]=float(mc[1]) if (mc and mc[1]!="nan") else float("nan")
            markers.append(d)
    return dict(csv=csv,frame=frame,rtt=rtt,markers=markers,frame_log=frame_log,baseline=baseline)


def windows(frame_log):
    """Geef (start_ms, stop_ms) paren uit START/STOP-events."""
    out=[]; start=None
    for state,t in frame_log:
        if state=="START": start=t
        elif state=="STOP" and start is not None: out.append((start,t)); start=None
    return out


# ---------- DV3 smoothness ----------

def smoothness(ts, vals):
    """Velocity-gebaseerde smoothness: median |v|, pieken>5x, jerk p99, %bewegend."""
    if len(vals)<3: return None
    vel=[]
    for i in range(len(vals)-1):
        dt=(ts[i+1]-ts[i])/1000.0
        if dt>0: vel.append((vals[i+1]-vals[i])/dt)
    vel=np.array(vel)
    moving=np.abs(vel)>1e-5
    mv=np.abs(vel[moving])
    if mv.size==0: return dict(moving_pct=0.0,med=0.0,spikes=0,spike_pct=0.0,jerk_p99=0.0)
    med=float(np.median(mv))
    spikes=int(np.sum(mv>5*med))
    jerk=np.abs(np.diff(vel))
    return dict(moving_pct=100*moving.mean(), med=med, spikes=spikes,
                spike_pct=100*spikes/mv.size, jerk_p99=float(np.percentile(jerk,99)))


# ---------- figuren ----------

def fig_pos_vs_tijd(data, outdir):
    frame=data["frame"]; csv=data["csv"]; wins=windows(data["frame_log"])
    if not frame or not wins:
        print("  (geen FRAME-data/venster -> positie-figuur overgeslagen)"); return
    lo,hi=max(wins,key=lambda w:w[1]-w[0])          # langste venster
    ft=np.array([t for t,*_ in frame if lo<=t<=hi]); fp=np.array([p for t,p,*_ in frame if lo<=t<=hi])
    samp=[(t,e,meas) for (t,e,k,v,d,meas) in csv if lo<=t<=hi]   # samples in venster
    t0=ft[0]
    plt.figure(figsize=(7.0,3.4))
    plt.plot((ft-t0)/1000.0, fp, "-", color="#1f6feb", lw=1.4, label="Kalman + dead-reckoning (display, 60 fps)")
    if samp:
        ct=np.array([s[0] for s in samp]); meas=np.array([s[2] for s in samp])
        if np.isfinite(meas).mean()>0.9:                         # nieuw meas_pos-veld aanwezig
            yy=meas; lab="gemeten samples (genorm. via calibratiemap)"
        else:                                                    # oude log: lineaire benadering
            ce=np.array([s[1] for s in samp],dtype=float)
            yy=(ce-ce.min())/(ce.max()-ce.min()) if ce.max()>ce.min() else ce*0
            lab="gemeten samples (encoder, lin. benadering)"
        plt.plot((ct-t0)/1000.0, yy, "o", color="#d1242f", ms=3.5, label=lab)
    plt.xlabel("tijd (s)"); plt.ylabel("genormaliseerde positie [0–1]")
    plt.title("Positie over tijd: gemeten samples vs. Kalman/dead-reckoning")
    plt.legend(loc="best",fontsize=8); plt.grid(alpha=0.25); plt.tight_layout()
    for ext in ("png","pdf"): plt.savefig(os.path.join(outdir,f"pos_vs_tijd.{ext}"),dpi=150)
    plt.close()
    print(f"  pos_vs_tijd: venster {(hi-lo)/1000:.1f}s, {len(ft)} frames, {len(samp)} samples")


def fig_rtt(data, outdir):
    rtt=np.array(data["rtt"])
    if rtt.size==0: print("  (geen BT_RTT -> RTT-figuur overgeslagen)"); return
    p95,p99=np.percentile(rtt,[95,99]); mean=rtt.mean()
    plt.figure(figsize=(7.0,3.4))
    hi=min(rtt.max(), np.percentile(rtt,99.5)*1.3)
    plt.hist(rtt, bins=60, range=(0,hi), color="#1f6feb", alpha=0.8)
    for v,c,lab in [(mean,"#2da44e","mean %.0f"%mean),(p95,"#bf8700","P95 %.0f"%p95),(p99,"#d1242f","P99 %.0f"%p99)]:
        plt.axvline(v,color=c,ls="--",lw=1.3,label=lab+" ms")
    plt.xlabel("Bluetooth round-trip (ms)"); plt.ylabel("aantal")
    plt.title("Bluetooth round-trip verdeling (n=%d)"%rtt.size)
    plt.legend(fontsize=8); plt.grid(alpha=0.25); plt.tight_layout()
    for ext in ("png","pdf"): plt.savefig(os.path.join(outdir,f"rtt_histogram.{ext}"),dpi=150)
    plt.close()
    print(f"  rtt_histogram: n={rtt.size} mean={mean:.0f} P95={p95:.0f} P99={p99:.0f} max={rtt.max():.0f} ms")


# ---------- samenvatting ----------

def summary(data, outdir):
    L=[]
    def out(s): L.append(s); print(s)
    out("="*64)
    out("SAMENVATTING")
    # RTT (DV1)
    rtt=np.array(data["rtt"])
    if rtt.size:
        p95,p99=np.percentile(rtt,[95,99])
        out(f"DV1 RTT: n={rtt.size} mean={rtt.mean():.0f} P95={p95:.0f} P99={p99:.0f} max={rtt.max():.0f} ms")
    # DV3 smoothness per as (over alle frame-vensters samen)
    fr=data["frame"]
    if fr:
        ts=[t for t,*_ in fr]
        for idx,name in [(1,"traction"),(2,"spindle"),(3,"swivel")]:
            r=smoothness(ts,[f[idx] for f in fr])
            if r: out(f"DV3 {name:8s}: bewegend {r['moving_pct']:4.0f}%  pieken>5x={r['spikes']} ({r['spike_pct']:.2f}%)  jerk p99={r['jerk_p99']:.4f}")
        dts=np.diff(ts)
        out(f"render: {len(fr)} frames, frame-interval mediaan {np.median(dts):.0f} ms (~{1000/np.median(dts):.0f} fps)")
    # Baseline
    if data["baseline"]:
        encs=[e for _,_,e in data["baseline"]]
        out(f"baseline-encoder: {min(encs)}..{max(encs)} (variatie {max(encs)-min(encs)})")
    # Markers (DV2)
    if data["markers"]:
        out("-"*64); out("DV2 markers:")
        out(f"{'MP':>3} {'label':<10} {'disp_mm':>9} {'fw_mm':>9} {'d-fw':>7} {'spin_kf':>8} {'swiv_kf':>8} {'compass':>8}")
        for m in data["markers"]:
            dmf=m['display_mm']-m['fw_mm']
            out(f"{int(m['n']):>3} {m['label']:<10} {m['display_mm']:>9.1f} {m['fw_mm']:>9.1f} {dmf:>7.1f} "
                f"{m['spindle_kf']:>8.2f} {m['swivel_kf']:>8.2f} {m['compass_yaw']:>8.2f}")
        out("  (display-vs-fysiek invullen met d_phys uit logboek; d-fw = pipeline-fout)")
    else:
        out("DV2 markers: (geen [MARKER] in deze log)")
    out("="*64)
    open(os.path.join(outdir,"samenvatting.txt"),"w").write("\n".join(L)+"\n")


def main():
    if len(sys.argv)<2:
        print(__doc__); sys.exit(1)
    path=sys.argv[1]
    outdir=sys.argv[2] if len(sys.argv)>2 else os.path.dirname(os.path.abspath(path)) or "."
    os.makedirs(outdir,exist_ok=True)
    data=parse(path)
    print(f"Geparsed: {len(data['csv'])} CSV, {len(data['frame'])} FRAME, {len(data['rtt'])} RTT, "
          f"{len(data['markers'])} markers, {len(windows(data['frame_log']))} frame-venster(s)")
    fig_pos_vs_tijd(data,outdir)
    fig_rtt(data,outdir)
    summary(data,outdir)
    print(f"\nUitvoer in: {outdir}")


if __name__=="__main__":
    main()
