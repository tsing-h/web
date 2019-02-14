// import Vue from 'vue'
import * as types from "./mutations_type";
import { MutationTree, Mutation } from "vuex";
import { State, CONFIG, GROUP, FIELD, Item } from "@/store";

const mutations: MutationTree<State> = {
  CHANGE_API_URL(state: State, new_url: string) {
    state.url_prefix = new_url;
    console.log("init", state.url_prefix);
  },
  // add template
  [types.ADD_TEMPLATE](state: State, payload: CONFIG) {
    state.template_list[payload.template_id] = { ...payload };
    // console.log("add", state.template_list);
  },
  // update template
  [types.UPDATE_TEMPLATE](state: State, payload: CONFIG) {
    // state.template_list[template_id].groups = { ...groups };
    state.template_list[payload.template_id] = { ...payload };
    console.log("update", payload);
  },
  // delete template
  [types.DELETE_TEMPLATE](state: State, { template_id }) {
    delete state.template_list[template_id];
    state.template_id = "";
    console.log("delete", template_id);
  },

  // add data
  [types.ADD_ITEMS](state: State, item: Item) {
    state.items.push(item);
    console.log("add_item", item);
  },
  // delete data
  [types.DEL_ITEMS](state: State, index: number) {
    // TODO
    delete state.items[index];
  },

  // init items
  [types.INIT_ITEMS](state: State, items: Item[]) {
    state.items = [...items];
  },

  // 设置当前模板
  [types.SELECT_TEMPLATE](state: State, template_id: string) {
    state.template_id = template_id;
    console.log("select template: ", template_id);
  },

  [types.SELECT_ITEM](state: State, index: number) {
    state.current_item = index;
  },

  [types.SHOW_ITEM](state: State, item: Item) {
    state.item_detail = { ...item };
    console.log("show detail info for data: ", item);
  },

  // add group
  [types.ADD_GROUP](state: State, group: any) {
    // state.template_id = template_id;
    state.template_list[state.template_id].groups.push(group);
    console.log("add template group: ", group);
  },
  // delete group
  [types.DELETE_GROUP](state: State, payload: any) {
    // TODO
  },
  // update group
  [types.UPDATE_GROUP](state: State, payload: any) {
    // TODO
  },
  // add field
  [types.ADD_FIELD](state: State, payload: any) {
    // TODO
  },
  // delete field
  [types.DELETE_FIELD](
    state: State,
    payload: { group_index: number; field_index: number }
  ) {
    state.template_list[state.template_id].groups[
      payload.group_index
    ].fields.splice(payload.field_index, 1);
    console.log(
      `delete the [${payload.field_index}th] field in the [` +
        `${payload.group_index}th] GROUP for TEMPLATE[${state.template_id}]\n`,
      payload,
      state.template_list[state.template_id]
    );
  }
};

export default mutations;
