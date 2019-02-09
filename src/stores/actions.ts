import { Commit, ActionTree, Action } from "vuex";
// import { Commit, Action, ActionTree } from 'vuex'
import * as types from "./mutations_type";
import { State, CONFIG, GROUP, FIELD, Item } from "@/store";

const url_prefix: string = "http://localhost:5000/clinicals";
const actions: ActionTree<State, any> = {
  [types.ACTION_SAVE_DATA]: (context: { commit: Commit }, payload: any) => {
    // 上传数据，触发
    console.log("save data in action: ", payload);
    context.commit(types.ADD_ITEMS, payload);
  },
  [types.ACTION_SAVE_GROUP]: (context: { commit: Commit }, payload: any) => {
    // 上传数据，触发
    console.log("save group in action: ", payload);
    // 1. 数据尚未存在，添加组
    // 2. 数据已存在，更新组
    context.commit(types.UPDATE_GROUP, payload);
  }
};

export default actions;
