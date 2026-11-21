(() => {
  "use strict";
  const MAX_BYTES = 32 * 1024 * 1024;
  const MAX_ATOMS = 200000;
  const canvas = document.getElementById("structure-canvas");
  const ctx = canvas.getContext("2d", { alpha: false });
  const status = document.getElementById("status");
  const empty = document.getElementById("empty-state");
  const selection = document.getElementById("selection");
  const atomList = document.getElementById("atom-list");
  const colourMode = document.getElementById("colour-mode");
  let atoms = [], selected = -1, yaw = 0.55, pitch = -0.35, zoom = 1, dragging = false, last = null, projected = [];
  const elementColours = {C:"#9aa9b5",N:"#5e9cf0",O:"#ed6a70",S:"#e6bd55",P:"#e69b55",H:"#e7edf0",F:"#75cda4",CL:"#75cda4"};
  const chainPalette = ["#71c9b7","#82a9ef","#e3b56b","#c58de1","#e88f9b","#a5c878","#7bc4dc","#e4a477"];
  const validNumber = n => typeof n === "number" && Number.isFinite(n);
  function validate(payload) {
    if (!payload || payload.schema !== "kinetics.structure-view.v1" || !["pdb","mmcif"].includes(payload.source_format) || payload.coordinate_unit !== "angstrom") throw new Error("Unsupported structure payload schema or units");
    if (!Array.isArray(payload.atoms) || payload.atoms.length < 1 || payload.atoms.length > MAX_ATOMS || payload.atom_count !== payload.atoms.length) throw new Error("Atom count is invalid or exceeds the viewer limit");
    if (!Array.isArray(payload.limitations) || !payload.limitations.length || payload.limitations.some(x => typeof x !== "string" || !x.trim())) throw new Error("Payload limitations are missing");
    const serials = new Set();
    for (const a of payload.atoms) {
      if (!a || !Number.isSafeInteger(a.serial) || a.serial < 0 || serials.has(a.serial) || !Number.isSafeInteger(a.residue_number) || a.residue_number < 0) throw new Error("Invalid or duplicate atom identifier");
      serials.add(a.serial);
      if (![a.name,a.residue,a.chain].every(x => typeof x === "string" && x.length <= 8) || typeof a.element !== "string" || !a.element.trim() || a.element !== a.element.trim().toUpperCase() || a.element.length > 3) throw new Error("Invalid atom annotation");
      if (!Array.isArray(a.xyz) || a.xyz.length !== 3 || !a.xyz.every(validNumber)) throw new Error("Invalid atom coordinates");
    }
  }
  function load(payload) {
    const bytes = new TextEncoder().encode(JSON.stringify(payload)).length;
    if (bytes > MAX_BYTES) throw new Error("Structure payload exceeds 32 MiB");
    validate(payload);
    atoms = payload.atoms.map(a => ({...a, xyz:a.xyz.slice()}));
    selected = -1; yaw = .55; pitch = -.35; zoom = 1;
    const count = atoms.length;
    empty.hidden = true;
    status.textContent = count.toLocaleString() + " atoms · " + payload.source_format.toUpperCase() + " · Å";
    atomList.replaceChildren();
    // Keep the accessible list bounded independently from the full coordinate set.
    atoms.slice(0, 500).forEach((a, i) => {
      const li = document.createElement("li");
      li.textContent = a.chain + ":" + a.residue + a.residue_number + " · " + a.name + " · #" + a.serial;
      li.addEventListener("click", () => { selected = i; updateSelection(); draw(); });
      atomList.append(li);
    });
    draw();
  }
  function resize() {
    const rect = canvas.getBoundingClientRect(), dpr = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = Math.max(1, Math.floor(rect.width*dpr)); canvas.height = Math.max(1, Math.floor(rect.height*dpr));
    ctx.setTransform(dpr,0,0,dpr,0,0); draw();
  }
  function atomColour(a) {
    if(colourMode.value==="chain"){let hash=0;for(const c of a.chain)hash=(hash*31+c.charCodeAt(0))|0;return chainPalette[Math.abs(hash)%chainPalette.length];}
    return elementColours[a.element]||"#9aa9b5";
  }
  function draw() {
    const w = canvas.clientWidth, h = canvas.clientHeight;
    if (!w || !h) return;
    ctx.fillStyle = "#0e1821"; ctx.fillRect(0,0,w,h); projected = [];
    if (!atoms.length) return;
    const bounds={min:[Infinity,Infinity,Infinity],max:[-Infinity,-Infinity,-Infinity]};
    for(const a of atoms)for(let axis=0;axis<3;axis++){bounds.min[axis]=Math.min(bounds.min[axis],a.xyz[axis]);bounds.max[axis]=Math.max(bounds.max[axis],a.xyz[axis]);}
    const center=bounds.min.map((value,axis)=>(value+bounds.max[axis])/2);
    const cy=Math.cos(yaw), sy=Math.sin(yaw), cp=Math.cos(pitch), sp=Math.sin(pitch);
    const rotated=atoms.map((a,i)=>{const x=a.xyz[0]-center[0],y=a.xyz[1]-center[1],z=a.xyz[2]-center[2];const x1=x*cy-z*sy,z1=x*sy+z*cy;return {i,x:x1,y:y*cp-z1*sp,z:y*sp+z1*cp};});
    let extent=1;for(const p of rotated)extent=Math.max(extent,Math.abs(p.x),Math.abs(p.y));
    extent*=2;
    const scale=Math.min(w,h)*.76/extent*zoom, ordered=rotated.slice().sort((a,b)=>a.z-b.z);
    for(const p of ordered){const a=atoms[p.i],x=w/2+p.x*scale,y=h/2-p.y*scale,r=p.i===selected?6:Math.max(1.8,Math.min(4,scale*.045));const colour=atomColour(a);
      const opacity=.55+(.45*(p.z/extent+0.5));
      ctx.beginPath();ctx.arc(x,y,r,0,Math.PI*2);ctx.fillStyle=colour;ctx.globalAlpha=opacity;ctx.fill();ctx.globalAlpha=1;
      if(p.i===selected){ctx.beginPath();ctx.arc(x,y,r+4,0,Math.PI*2);ctx.strokeStyle="#ffffff";ctx.lineWidth=1.5;ctx.stroke();}
      projected[p.i]={x,y,z:p.z,r,opacity};
    }
  }
  function getState() {
    return {
      schema:"kinetics.structure-view-state.v1",
      yaw,
      pitch,
      zoom,
      colour_mode:colourMode.value,
      selected_atom_serial:selected>=0?atoms[selected].serial:null
    };
  }
  function setState(state) {
    if(!state||state.schema!=="kinetics.structure-view-state.v1"||
       !validNumber(state.yaw)||!validNumber(state.pitch)||!validNumber(state.zoom)||
       state.pitch < -1.5||state.pitch > 1.5||state.zoom < .2||state.zoom > 8||
       !["element","chain"].includes(state.colour_mode)) throw new Error("Invalid viewer state");
    if(state.selected_atom_serial!==null&&
       (!Number.isSafeInteger(state.selected_atom_serial)||state.selected_atom_serial<0)) {
      throw new Error("Invalid selected atom serial");
    }
    yaw=state.yaw;pitch=state.pitch;zoom=state.zoom;colourMode.value=state.colour_mode;
    selected=state.selected_atom_serial===null?-1:
      atoms.findIndex(atom=>atom.serial===state.selected_atom_serial);
    updateSelection();draw();return getState();
  }
  function exportSvg() {
    if(!atoms.length) throw new Error("No structure is loaded");
    if(projected.length!==atoms.length||projected.some(point=>!point)) draw();
    const width=Math.max(1,canvas.clientWidth),height=Math.max(1,canvas.clientHeight);
    const parts=[
      '<svg xmlns="http://www.w3.org/2000/svg" width="'+width+'" height="'+height+
      '" viewBox="0 0 '+width+' '+height+'">',
      '<rect width="100%" height="100%" fill="#0e1821"/>'
    ];
    for(let i=0;i<atoms.length;i++){
      const point=projected[i];if(!point)continue;
      const colour=atomColour(atoms[i]);
      parts.push('<circle cx="'+point.x.toFixed(3)+'" cy="'+point.y.toFixed(3)+
        '" r="'+point.r.toFixed(3)+'" fill="'+colour+'" fill-opacity="'+
        point.opacity.toFixed(4)+'"/>');
      if(i===selected)parts.push('<circle cx="'+point.x.toFixed(3)+'" cy="'+
        point.y.toFixed(3)+'" r="'+(point.r+4).toFixed(3)+
        '" fill="none" stroke="#ffffff" stroke-width="1.5"/>');
    }
    parts.push("</svg>");
    const svg=parts.join("");
    if(new TextEncoder().encode(svg).length>MAX_BYTES) throw new Error("SVG exceeds 32 MiB");
    return svg;
  }
  function updateSelection(){const a=atoms[selected];selection.textContent=a?"Chain "+(a.chain||"—")+" · "+a.residue+a.residue_number+" · "+a.name+" · atom #"+a.serial:"No atom selected";Array.from(atomList.children).forEach((li,i)=>li.setAttribute("aria-current",String(i===selected)));}
  canvas.addEventListener("pointerdown",e=>{dragging=true;last={x:e.clientX,y:e.clientY};canvas.setPointerCapture(e.pointerId);});
  canvas.addEventListener("pointermove",e=>{if(!dragging||!last)return; yaw+=(e.clientX-last.x)*.008;pitch=Math.max(-1.5,Math.min(1.5,pitch+(e.clientY-last.y)*.008));last={x:e.clientX,y:e.clientY};draw();});
  canvas.addEventListener("pointerup",e=>{dragging=false;last=null;const rect=canvas.getBoundingClientRect(),x=e.clientX-rect.left,y=e.clientY-rect.top;let best=-1,distance=18;projected.forEach((p,i)=>{if(!p)return;const d=Math.hypot(p.x-x,p.y-y);if(d<distance){distance=d;best=i;}});if(best>=0){selected=best;updateSelection();draw();}});
  canvas.addEventListener("wheel",e=>{e.preventDefault();zoom=Math.max(.2,Math.min(8,zoom*(e.deltaY<0?1.1:.9)));draw();},{passive:false});
  colourMode.addEventListener("change",draw);
  document.getElementById("reset-view").addEventListener("click",()=>{yaw=.55;pitch=-.35;zoom=1;draw();});
  window.addEventListener("resize",resize);
  // Deliberately no generic native bridge, eval hook, network loader or file access.
  const structureViewerApi = Object.freeze({
    load,exportSvg,getState,setState,
    clear(){atoms=[];selected=-1;projected=[];atomList.replaceChildren();empty.hidden=false;status.textContent="Waiting for structure payload";updateSelection();draw();}
  });
  resize();
  window.MolecularisStructureViewer = structureViewerApi;
  // Backward-compatible global for previously embedded viewer clients.
  window.KineticsStructureViewer = structureViewerApi;
})();