<template>
  <div class="container-flex">
    <div class="row border-top mt-3 ">
      <!-- 编辑模板 -->
      <div class="col pl-0 my-1" v-if="editable">
        <label class="h4 float-left mt-2">模板名称:</label>
        <el-input v-model="config.name" placeholder="请修改模板名称" :class="'w-25 float-left ml-2'" required></el-input>

        <el-button class="el-icon-refresh float-right ml-2" @click="save_template"> 保存模板</el-button>
        <el-button class="el-icon-plus float-right" @click="add_group"> 添加Group</el-button>
      </div>
      <!-- 可以填写表单数据 -->
      <div class="col pl-0 my-1" v-if="!editable">
        <label class="h4 float-left mt-2">模板名称: {{ config.name }}</label>

        <el-button class="el-icon-refresh float-right ml-2" @click="save_data"> 保存数据</el-button>
        <el-button class="el-icon-edit float-right" @click="editable=!editable"> 编辑模板</el-button>
        <el-button class="el-icon-delete float-right" @click="delete_template"> 删除模板</el-button>
      </div>
      <div class="w-100 ">  </div>

      <!-- 模板上下文 GROUP -->
      <div class="card border w-100 mb-2"  v-for="(group, index_group) in config.groups" :key="index_group">
        <!-- 组名 -->
        <div class="card-header align-items-start" v-if="!editable">
          <label class="h4 float-left mt-2">组名: {{ config.groups[index_group].name }}</label>

          <el-button class="el-icon-arrow-down float-right ml-2" > 展开</el-button>
          <el-button class="el-icon-refresh float-right ml-2" > 更新</el-button>
        </div>
        <!-- 编辑组 -->
        <div class="card-header align-items-start" v-if="editable">
          <label class="h4 float-left mt-2">组名:</label>
          <el-input v-model="config.groups[index_group].name" placeholder="请修改组名" :class="'w-25 float-left ml-2'"></el-input>

          <el-button class="el-icon-delete float-right ml-2" @click="config.groups.splice(index_group,1);$forceUpdate()"> 移除</el-button>
          <el-button class="el-icon-plus float-right" @click="cur_group=cur_group==index_group?-1:index_group"> 添加Field</el-button>
        </div>

        <ul class="list-group list-group-flush">
          <!-- 添加组字段 -->
          <el-collapse-transition>
          <li class="list-group-item text-left" >
            <code> {{ group }}</code>
          </li>
          </el-collapse-transition>
          <li class="list-group-item text-left" v-if="cur_group == index_group">
            <el-collapse-transition>
              <FieldGenerate v-model="tmp_field" @submit="addfield" />
            </el-collapse-transition>
          </li>
          <!-- 渲染模板 -->
          <li class="list-group-item text-left" v-for="(field, index) in group.fields" :key="index">
            <FieldRender v-bind:field="field" />
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Watch, Vue } from "vue-property-decorator";
import axios from "axios";
import FieldGenerate from "@/components/FieldGenerate.vue";
import FieldRender from "@/components/FieldRender.vue";
Vue.component("FieldGenerate", FieldGenerate);
Vue.component("FieldRender", FieldRender);

@Component
export default class Test extends Vue {
  @Prop() private msg!: string;
  @Prop() private config!: any;
  @Prop() private edit!: boolean;

  @Watch("config")
  onConfigChanged(val: any, oldVal: any) {
    this.edit = false;
    this.editable = false;
    this.cur_group = -1;
    this.tmp_field = {};
    // this.config = { ...this.template_config };
  }

  url_prefix: string = "http://localhost:5000/clinicals";
  // config: any = { ...this.template_config };
  editable: boolean = this.edit;
  tmp_field: any = {};

  // addfield: boolean = false;
  cur_group: number = -1;

  save_data() {}

  delete_template() {
    axios.get(`${this.url_prefix}/${this.config.templateid}/delete`);
  }
  save_template() {
    this.editable = !this.editable;
  }

  addfield(field: any) {
    if (!this.config["groups"][this.cur_group].fields)
      this.config["groups"][this.cur_group].fields = [];
    this.config["groups"][this.cur_group].fields.push(field);
    this.cur_group = -1;
  }

  add_group() {
    if (!this.config["groups"]) this.config["groups"] = [];
    // this.formdata["group" + this.config["groups"].length] = {};
    this.config["groups"].push({});
    this.$forceUpdate();
  }

  // 生命周期函数
  // created() {
  //   console.log("created");
  // }
  // mounted() {
  //   console.log("mounted");
  // }
  // updated() {
  //   console.log("updated");
  // }
  // destroyed() {
  //   console.log("destroyed");
  // }
}
</script>
