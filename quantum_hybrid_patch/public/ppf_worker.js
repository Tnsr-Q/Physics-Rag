
import init, { analyze_ppf } from './pkg/wasm_ppf_core.js';

let ready = false;
init().then(() => { ready = true; });

onmessage = ({ data }) => {
  if (!ready) return;
  const input = JSON.stringify({ quasienergies: data });
  const jsonResult = analyze_ppf(input);
  postMessage(JSON.parse(jsonResult));
};
