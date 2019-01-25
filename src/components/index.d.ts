interface FIELD {
  name: string;
  label: string;
  type: string;
  fields: [FIELD];
}

interface VALUE {
  value: string | number;
  subs: any;
}

interface GROUP {
  name: string;
  label: string;
  default: number | string;
  fields: any;
}

interface CFG {
  name: string;
  url: string;
  groups: any;
}
interface CFGLST {
  [cfgname: string]: CFG;
}
