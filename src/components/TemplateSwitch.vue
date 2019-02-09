<template>
  <div class="col mx-0 px-0">
    <el-select 
      v-model="cur_template" 
      placeholder="选择模板" 
      @change="change_template" 
      :class="!add ? 'col mx-0 px-0' : 'col-auto  px-0'"
      :name = "'template_id'"
    >
      <!-- :popper-append-to-body="false" -->
        <el-option
          v-for="(item, key) in $store.state.template_list"
          :key="item.name"
          :label="item.name"
          :value="key">
        </el-option>
      </el-select>
      <el-button class="el-icon-plus col-auto " @click="add_template" v-if="add"> 新建模板</el-button>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue, Watch } from "vue-property-decorator";
import store, { State, CONFIG } from "../store";
import * as types from "../stores/mutations_type";
import { mapState } from "vuex";
import axios from "axios";

@Component
export default class TemplateSwitch extends Vue {
  // 指示在哪里获取模板列表
  @Prop() private url!: string;
  // 指示是否支持创建新模板
  @Prop() private add!: boolean;

  // 组件数据交互 v-model功能需要有个Prop：value，以及适当情况下$emit("input", value)

  cur_template: string = "";
  // 从state中继承 template_list, config, template_id

  // template_list: $store.state.template_list;
  // template_list: {
  //   [name: string]: CONFIG;
  // } = this.$store.state.template_list;
  // config: any = this.$store.getters.config;

  created() {
    axios
      .get(this.url)
      .then(rsp => {
        let data = rsp.data.data;
        // console.log(data);
        for (const key in data) {
          // const element = data[key];
          // element.name = element.template_name;
          let config: CONFIG = {
            name: data[key].template_name,
            url: data[key].url,
            template_id: data[key].templateid,
            groups: []
          };
          this.$store.commit(types.ADD_TEMPLATE, config);
          this.$forceUpdate();
        }
        // this.template_list = data;
        // this.$store.commit("init_template", data);
      })
      .catch(e => {
        // this.template_list = {};
      });
  }

  add_template() {
    const templateid =
      "template_" +
      Math.random()
        .toString(36)
        .slice(-8);
    const config: CONFIG = {
      name: templateid,
      url: "",
      template_id: templateid,
      groups: []
    };
    this.$store.dispatch("add_template", config);
    this.$forceUpdate();
  }

  // 切换模板时，根据url获取模板
  change_template(template_key) {
    if (template_key in this.$store.state.template_list) {
      let config = this.$store.state.template_list[template_key];
      if (!config.groups.length && config.url) {
        axios.get(config.url).then(rsp => {
          config.groups = rsp.data.data.groups;
          this.$store.commit(types.UPDATE_TEMPLATE, config);
          this.$store.commit(types.SELECT_TEMPLATE, config.template_id);
          this.$forceUpdate();
        });
      } else {
        this.$store.commit(types.SELECT_TEMPLATE, config.template_id);
      }
    }
  }
}
</script>
