<template>
  <div class="container-flex">
    
    <TemplateSwitch v-bind:url="'http://localhost:5000/clinicals/templatelist'" :add="false" class="col w-100 " />
    <FormRender msg="this is test" v-bind:editable="true" v-if="$store.getters.config.template_id" :item="$store.state.item_detail"></FormRender>
    <div class="row">
      <el-select v-model="cur_template" placeholder="选择已有模板" @change="change_template">
        <el-option
          v-for="(item, key) in template_list"
          :key="item.name"
          :label="item.name"
          :value="key">
        </el-option>
      </el-select>
      <el-button class="el-icon-plus" @click="add_template"> 新建模板</el-button>
    </div>
    <Test msg="this is test" v-bind:config="config" v-bind:edit="false" v-if="config.templateid"></Test>
    <!-- <FormTemplate  v-bind:template_config="config" v-bind:editable="editable" v-if="cur_template"/> -->
  </div>
</template>

<script lang="ts">
// 1. 选择模板 或 创建模板
// 2.
import { Component, Vue } from "vue-property-decorator";
// import ClinicalTemplate from "@/components/ClinicalTemplate.vue"; // @ is an alias to /src
import axios from "axios";
import Element from "element-ui";
import "element-ui/lib/theme-chalk/index.css";
Vue.use(Element);

import FormTemplate from "@/components/FormTemplate.vue"; // @ is an alias to /src
import Test from "@/components/Test.vue";

import TemplateSwitch from "@/components/TemplateSwitch.vue";
import FormRender from "@/components/FormRender.vue";

@Component({
  components: {
    // ClinicalTemplate
    FormTemplate,
    Test,
    TemplateSwitch,
    FormRender
  }
})
export default class Template extends Vue {
  cur_template: string = "";
  template_list: {
    [name: string]: {
      name: string;
      url: string;
      templateid: string;
      groups: any;
    };
  } = {};
  config: any = {};
  url_prefix: string = "http://localhost:5000/clinicals";
  url_save_template: string = this.url_prefix + "/savetemplate/";

  created() {
    axios
      .get(this.url_prefix + "/templatelist")
      .then(rsp => {
        let data = rsp.data.data;
        // console.log(data);
        for (const key in data) {
          const element = data[key];
          element.name = element.template_name;
        }
        this.template_list = data;
      })
      .catch(e => {
        this.template_list = {};
      });
  }

  add_template() {
    const templateid =
      "template_" +
      Math.random()
        .toString(36)
        .slice(-8);
    this.template_list[templateid] = {
      name: templateid,
      url: "",
      groups: [],
      templateid: templateid
    };
    this.cur_template = templateid;
    this.config = this.template_list[templateid];
    this.$forceUpdate();
  }

  // 切换模板时，根据url获取模板
  change_template(template_key) {
    if (template_key in this.template_list) {
      let config = this.template_list[template_key];
      if (!config.groups && config.url) {
        axios.get(config.url).then(rsp => {
          console.log(rsp);
          config.groups = rsp.data.data.groups;
          this.config = config;
        });
      } else {
        this.config = config;
      }
    }
  }
}
</script>
