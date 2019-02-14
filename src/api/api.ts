export function request(params: any) {
  // TODO
}

import request2 from "../plugins/axios";

export function loginByUsername(username, password) {
  const data = {
    username,
    password
  };
  return request({
    url: "/login/login",
    method: "post",
    data
  });
}
