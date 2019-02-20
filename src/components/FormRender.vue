<template>
  <div :class="'w-100'">
    <!-- 模板头 -->
    <div class="col pl-0 my-1" v-if="!editable">
      <label class="h4 float-left mt-2">模板: {{ config.name }}</label>

      <el-button class="el-icon-refresh float-right ml-2" @click="save_data"> 保存</el-button>
    </div>
    <div class="col-full px-0 my-1" v-else>
      <div class="alert alert-danger no-gutter ">正在修改模板...</div>
      <div class="row">
        <div class="input-group col-8">
          <div class="input-group-prepend">
            <span class="input-group-text">模板名称</span>
          </div>
          <input type="text" v-model="config.name" class="form-control" style="height:40px">
        </div>
        <el-button class="col el-icon-plus  " @click="add_group"> 添加组</el-button>
        <el-button class="col el-icon-delete" type="danger" @click="delete_template"> 删除模板</el-button>
        <el-button class="col el-icon-refresh mr-3" @click="save_template"> 保存模板</el-button>
      </div>
    </div>
    <div class="w-100 ">  </div>

    <GroupRender 
      v-for="(group, index_group) in config.groups" :key="index_group"
      :group="group"
      :index_group="index_group"
      :item="group_data(group)"
      :editable="editable"
      class="w-100"
      v-model="formdata[group.name]"
      @destroyed="$forceUpdate()"
      v-on:submit="save_data"
    />
  </div>
</template>

<script lang="ts">
import { Component, Prop, Watch, Vue } from "vue-property-decorator";
import axios from "axios";
import GroupRender from "@/components/GroupRender.vue";

import { CONFIG, Item } from "../store";
import * as types from "../stores/mutations_type";

@Component({
  components: { GroupRender }
})
export default class FormRender extends Vue {
  @Prop() private editable!: boolean;

  public get config(): CONFIG {
    return this.$store.getters.config;
  }

  @Prop() private item!: Item;

  @Watch("config")
  onConfigChanged(val: any, oldVal: any) {
    // this.editable = false;
    // this.editable = false;
    this.formdata = {};
  }

  formdata: any = {};

  save_data() {
    console.log("save data", this.formdata);
    // this.$store.commit(types.ADD_ITEMS, this.formdata);
    this.$store.dispatch(types.ACTION_SAVE_DATA, this.formdata);
    this.$forceUpdate();
    // this.anydata.
  }

  group_data(group) {
    let o = {};
    let refdata = this.item;
    if (!this.item || Object.keys(this.item).length == 0) {
      refdata = this.formdata;
    }
    // group.fields.map(e => e.name);
    if (group.fields) {
      group.fields.forEach(({ name }) => {
        o[name] = refdata[name];
      });
    }
    return o;
  }

  // 当处于编辑模板场景时:
  add_group() {
    this.$store.commit(types.ADD_GROUP, { name: "", fields: [] });
    this.$forceUpdate();
  }

  delete_template() {
    this.$store.dispatch(types.ACTION_DELETE_TEMPLATE, {
      template_id: this.config.template_id
    });
  }

  save_template() {
    // 检查模板信息是否符合规定
    if (this.config.name === "template_unknown_name") {
      this.$message({ type: "error", message: "请修改模板名称" });
      return;
    }
    this.$store.dispatch(types.ACTION_UPDATE_TEMPLATE, {
      template_id: this.config.template_id
    });
  }
}
</script>
