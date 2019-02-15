<template>
  <div class="input-group">
    <el-select 
      v-model="cur_template" 
      placeholder="选择模板" 
      @change="change_template" 
      :class="'col mx-0 px-0'"
      :name = "'template_id'"
    >
      <!-- :popper-append-to-body="false" -->
      <el-option
        v-for="(item, key) in template_list"
        :key="key"
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
  template_list: {
    [name: string]: CONFIG;
  } = {};

  @Watch("$store.state.template_id")
  HandleChange(newVal, oldVal) {
    this.cur_template = newVal;
  }

  created() {
    // const _template_list: string[] = [];
    this.cur_template = this.$store.state.template_id;
    this.template_list = this.$store.state.template_list;
    if (!this.cur_template) {
      this.$store
        .dispatch(types.ACTION_INIT_TEMPLATE_LIST, { url: this.url })
        .then(() => {
          console.log(
            "init template list end",
            this.$store.state.template_list
          );
          this.template_list = this.$store.state.template_list;
          this.$forceUpdate();
        });
    }
  }

  add_template() {
    const config: CONFIG = {
      name: "template_unknown_name",
      url: "",
      template_id: "template_unknown_id",
      groups: []
    };
    this.$store.commit(types.ADD_TEMPLATE, config);
    this.$forceUpdate();
    this.$message({ type: "warning", message: "模板已添加，请及时更新" });
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
