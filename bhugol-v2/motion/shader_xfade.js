/* BHUGOL shader transition overlay (3D template). Ported from @hyperframes/shader-transitions 0.8.181 (MIT): the GLSL is
   the package's, the driver is ours. Why not HyperShader.init(): that switches the WHOLE render to HyperFrames' layered
   screenshot route (~5 s/frame here, an 85 s video would take hours). This overlay only costs the ~0.8 s of the cut.

   const XF = BhugolXfade(THREE, document.getElementById('cshake'));
   XF.add(t0, dur, {cv: fromCanvas, push: fromPushEl}, {cv: toCanvas, push: toPushEl}, 'burn');
   ...in the render driver, after every scene canvas is drawn for time t:  XF.render(t);
   The push elements' scale (punch-ins) is matched in the shader so the swap has no jump.
   Shaders: burn (ridged fire burn, toned down for full-frame plates). Add more from the package the same way. */
(function (G) {
  const HEAD = `varying vec2 v_uv; uniform sampler2D u_from, u_to; uniform float u_progress, sA, sB; uniform vec2 u_resolution; uniform vec3 u_accent, u_accent_dark, u_accent_bright;
float hash(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}
float vnoise(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*f*(f*(f*6.-15.)+10.);return mix(mix(hash(i),hash(i+vec2(1,0)),f.x),mix(hash(i+vec2(0,1)),hash(i+vec2(1,1)),f.x),f.y);}
vec4 A_(){ vec2 o = vec2(.5,.55); return texture2D(u_from,(v_uv-o)/sA+o); } vec4 B_(){ vec2 o = vec2(.5,.55); return texture2D(u_to,(v_uv-o)/sB+o); }`;
  const SH = {
    // ridged-burn (package values: heat x3.5, white core from .5) toned to x2.2 / white from .7 so the frame never blows out
    burn: HEAD + `float ridged(vec2 p){float v=0.,a=.5;mat2 R=mat2(.8,.6,-.6,.8);for(int i=0;i<5;i++){v+=a*abs(vnoise(p)*2.-1.);p=R*p*2.02;a*=.5;}return v;}
void main(){ vec4 A=A_(), B=B_(); float n=ridged(v_uv*vec2(4.,7.1));
float e=smoothstep(u_progress-.04,u_progress+.04,n); float heat=smoothstep(.09,0.,abs(n-u_progress))*(1.-step(1.,u_progress));
vec3 burn=mix(u_accent_dark,u_accent,smoothstep(0.,.25,heat)); burn=mix(burn,u_accent_bright,smoothstep(.3,.6,heat)); burn=mix(burn,vec3(1),smoothstep(.7,1.,heat));
float sparks=step(.93,vnoise(v_uv*vec2(80.,142.)))*heat*2.; gl_FragColor=vec4(mix(B,A,e).rgb+burn*heat*2.2+u_accent_bright*sparks,1.); }`
  };
  G.BhugolXfade = function (T3, parent) {
    const cv = document.createElement('canvas'); cv.width = 1080; cv.height = 1920; cv.className = 'cv'; cv.id = 'xfade'; cv.style.opacity = 0; parent.appendChild(cv);
    const R = new T3.WebGLRenderer({ canvas: cv, preserveDrawingBuffer: true }); R.setPixelRatio(1); R.setSize(1080, 1920, false);
    const U = { u_from: { value: null }, u_to: { value: null }, u_progress: { value: 0 }, u_resolution: { value: new T3.Vector2(1080, 1920) }, sA: { value: 1 }, sB: { value: 1 },
      u_accent: { value: new T3.Vector3(1, .42, .08) }, u_accent_dark: { value: new T3.Vector3(.35, .05, 0) }, u_accent_bright: { value: new T3.Vector3(1, .86, .45) } };
    const cam = new T3.OrthographicCamera(-1, 1, 1, -1, 0, 1), scenes = {};
    const sceneFor = k => scenes[k] || (scenes[k] = (() => { const s = new T3.Scene(); s.add(new T3.Mesh(new T3.PlaneGeometry(2, 2), new T3.ShaderMaterial({ uniforms: U, depthTest: false,
      vertexShader: 'varying vec2 v_uv; void main(){ v_uv = uv; gl_Position = vec4(position.xy, 0.0, 1.0); }', fragmentShader: SH[k] || SH.burn }))); return s; })());
    const EZ = gsap.parseEase('power2.inOut'), X = { list: [], cv };
    X.add = (t0, dur, from, to, kind) => { X.list.push({ t0, dur, from, to, k: kind || 'burn', tA: new T3.CanvasTexture(from.cv), tB: new T3.CanvasTexture(to.cv) }); sceneFor(kind || 'burn'); };
    X.render = t => { const b = X.list.find(b => t >= b.t0 && t < b.t0 + b.dur); cv.style.opacity = b ? 1 : 0; if (!b) return;
      b.tA.needsUpdate = b.tB.needsUpdate = true; U.u_from.value = b.tA; U.u_to.value = b.tB; U.u_progress.value = -.06 + 1.14 * EZ((t - b.t0) / b.dur);
      U.sA.value = gsap.getProperty(b.from.push, 'scale') || 1; U.sB.value = gsap.getProperty(b.to.push, 'scale') || 1; R.render(sceneFor(b.k), cam); };
    return X;
  };
})(window);
