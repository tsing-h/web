<template>
  <div class=" w-100">
    <!-- 模板头 -->
    <div class="col pl-0 my-1" v-if="!editable">
      <label class="h4 float-left mt-2">模板: {{ config.name }}</label>

      <el-button class="el-icon-refresh float-right ml-2" @click="save_data"> 保存</el-button>
    </div>
    <div class="w-100 ">  </div>

    <GroupRender 
      v-for="(group, index_group) in config.groups" :key="index_group"
      :group="group"
      :index_group="index_group"
      class="w-100"
      v-model="formdata[group.name]"
    />
  </div>
</template>

<script lang="ts">
import { Component, Prop, Watch, Vue } from "vue-property-decorator";
import axios from "axios";
import GroupRender from "@/components/GroupRender.vue";

import { CONFIG } from "../store";
import * as types from "../stores/mutations_type";

@Component({
  components: { GroupRender }
})
export default class FormRender extends Vue {
  @Prop() private edit!: boolean;
  public get config(): CONFIG {
    return this.$store.getters.config;
  }

  @Watch("config")
  onConfigChanged(val: any, oldVal: any) {
    this.edit = false;
    this.editable = false;
    this.formdata = {};
  }
  formdata: any = {};
  save_data() {
    // this.$store.commit(types.ADD_ITEMS, this.formdata);
    this.$store.dispatch(types.ACTION_SAVE_DATA, this.formdata);
  }

  // 当处于编辑模板场景时:
  editable: boolean = this.edit;

  delete_template() {
    const url_prefix: string = "http://localhost:5000/clinicals";
    axios.get(`${url_prefix}/${this.config.template_id}/delete`);
    this.$store.commit(types.DELETE_TEMPLATE, this.config.template_id);
  }

  save_template() {
    this.editable = !this.editable;
    // TODO ...
  }
}
</script>
