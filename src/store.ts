import Vue from "vue";
import Vuex, { Commit, Mutation, Action } from "vuex";
import axios from "./plugins/axios";
import * as types from "./stores/mutations_type";
import mutations from "./stores/mutations";
import actions from "./stores/actions";

Vue.use(Vuex);

export interface FIELD {
  name: string;
  label?: string;
  type: string;
  value?: any;
}
export interface GROUP {
  name: string;
  fields: FIELD[];
}
// 模板配置信息
export interface CONFIG {
  name: string;
  url: string;
  template_id: string;
  groups: GROUP[];
}

export interface Item {
  [key: string]: string | number;
}

export interface State {
  // 表格数据
  items: Item[];
  // 模板信息
  template_id: string;
  template_list: { [template_id: string]: CONFIG };
  // 分页
  page: number;
  page_size: number;
  // 数据详情页当前条目数据索引
  current_item: number;
  item_detail: Item;
  url_prefix: string;
}

const state: State = {
  items: [],
  template_id: "",
  template_list: {},
  page: 0,
  page_size: 10,
  current_item: 0,
  item_detail: {},
  url_prefix: "http://localhost:5000/clinicals"
};

let getters = {
  // 获取当前配置信息
  config: (state: State) => {
    return state.template_id ? state.template_list[state.template_id] : {};
  }
  // 根据索引获取指定元素
  // item: (state: State, index: number) => state.items[index]
};

// let actions = {
//   // 添加新的模板, 同时设定当前选中的模板
//   add_template(context: { commit: Commit; state: State }, config: CONFIG) {
//     context.commit(types.ADD_TEMPLATE, config);
//     context.commit(types.SELECT_TEMPLATE, config.template_id);
//   }
// };

export default new Vuex.Store({
  state,
  getters,
  mutations,
  actions
});
