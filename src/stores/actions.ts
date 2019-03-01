import { Commit, ActionTree, Action } from "vuex";
// import { Commit, Action, ActionTree } from 'vuex'
import * as types from "./mutations_type";
import { State, CONFIG, GROUP, FIELD, Item } from "@/store";

import axios from "axios";
import { Message, Notification } from "element-ui";

const url_prefix: string = "http://192.168.1.251:5000/clinicals";
const actions: ActionTree<State, any> = {
  [types.ACTION_INIT_TEMPLATE_LIST]: (context: { commit: Commit }, { url }) => {
    // console.log("fetch template list in action: ", url);
    return axios.get(url).then(rsp => {
      let data = rsp.data.data;
      // console.log(data);
      for (const key in data) {
        let config: CONFIG = {
          name: data[key].template_name,
          url: data[key].url,
          template_id: data[key].templateid,
          groups: []
        };
        context.commit(types.ADD_TEMPLATE, config);
      }
    });
  },

  [types.ACTION_UPDATE_TEMPLATE]: (
    context: { commit: Commit; state: State },
    { template_id }
  ) => {
    // 上传模板配置到后台
    const cfg: CONFIG = context.state.template_list[template_id];
    return axios
      .post(`${url_prefix}/template/${template_id}`, JSON.stringify(cfg))
      .then(rsp => {
        const data: any = rsp.data;
        const { status, msg, templateid } = rsp.data;
        // console.log(data.code);
        if (status != "success") {
          Message({
            type: "error",
            message: msg
          });
        } else {
          const msg: string = JSON.stringify(rsp.data);
          // 新增模板时，需要更改本地配置
          if (template_id != templateid) {
            cfg.template_id = templateid;
            // context.commit(types.SELECT_TEMPLATE, templateid);
            context.commit(types.DELETE_TEMPLATE, template_id);
            context.commit(types.ADD_TEMPLATE, cfg);
          }

          Message({
            type: "success",
            message: `模板${templateid}配置已保存`
          });
        }
      })
      .catch(err => {
        Message.error("未知错误");
      });
  },

  [types.ACTION_DELETE_TEMPLATE]: (
    context: { commit: Commit; state: State },
    { template_id }
  ) => {
    // console.log("delete template in action: ", context.state.template_id);
    // 上传模板配置到后台
    return axios
      .get(`${context.state.url_prefix}/template/${template_id}/delete`)
      .then(() => {
        context.commit(types.DELETE_TEMPLATE, { template_id });
        Message({
          type: "success",
          message: "已删除"
        });
      });
  },

  [types.ACTION_SAVE_DATA]: (
    context: { commit: Commit; state: State },
    payload: any
  ) => {
    axios
      .post(context.state.url_prefix + "/add", { data: payload })
      .then(rsp => {
        Message({
          type: "success",
          message: "数据已保存"
        });
      })
      .catch((err: Error) => {
        Notification({
          type: "error",
          title: err.name,
          dangerouslyUseHTMLString: true,
          message: `<code>${err.message}</code>`,
          duration: 5000
        });
      });

    context.commit(types.ADD_ITEMS, payload);
  },

  [types.ACTION_FETCH_ITEM]: ({ commit, state }, item_id) => {
    return new Promise((res, rej) => {
      //
      axios
        .get(`${state.url_prefix}/data/${item_id}`)
        .then(rsp => {
          const item = rsp.data.data;
          commit(types.SHOW_ITEM, item);
          res(item);
        })
        .catch(reason => {
          rej(reason);
        });
    });
  },

  [types.ACTION_DELETE_ITEM]: ({ commit, state }, { index, id }) => {
    return axios.get(`${state.url_prefix}/data/${id}/delete`);
  },

  [types.ACTION_SAVE_GROUP]: (
    context: { commit: Commit; state: State },
    payload: any
  ) => {
    // 减少与store交互的组件
    // 子组件通过submit事件，触发父组件的ACTION_SAVE_DATA
  },

  [types.SHOW_ITEM]: (context: { commit: Commit }, item: any) => {
    // 上传数据，触发
    // console.log("show detail info for data: ", item);
    // 1. 数据尚未存在，添加组
    // 2. 数据已存在，更新组
    // context.commit(types.UPDATE_GROUP, item);
  }
};

export default actions;
