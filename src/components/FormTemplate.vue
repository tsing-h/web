/* eslint-disable no-console */
<template>
  <div class="container-flex">
    <!-- 模板内容 -->
    <div class="row border-top mt-3 " v-if="cur_template">
      <!-- 模板名称 && 可选操作 -->
      <div class="col pl-0 my-1">
        <label class="h4 float-left mt-2">模板名称:</label>
        <el-input v-model="template_list[cur_template].name" placeholder="请修改模板名称" :class="'w-25 float-left ml-2'"></el-input>

        <el-button class="el-icon-refresh float-right ml-2" @click="save_template"> 保存</el-button>
        <el-button class="el-icon-plus float-right" @click="add_group"> 添加Group</el-button>
      </div>
      <div class="w-100 border border-warning"> <code>{{ JSON.stringify(config) }}</code> </div>
      <!-- 模板组 -->
      <div class="card border w-100 mb-2"  v-for="(group, index_group) in config.groups" :key="index_group">
        <!-- 组名 && 操作 -->
        <div class="card-header align-items-start">
          <label class="h4 float-left mt-2">组名:</label>
          <el-input v-model="config.groups[index_group].name" placeholder="请修改组名" :class="'w-25 float-left ml-2'"></el-input>

          <el-button class="el-icon-delete float-right ml-2" @click="config.groups.splice(index_group,1)"> 移除</el-button>
          <el-button class="el-icon-plus float-right" @click="add=add==index_group?-1:index_group"> 添加Field</el-button>
        </div>

        <ul class="list-group list-group-flush">
          <!-- test -->
          <!-- <li class="list-group-item">{{ cur_field }}</li> -->
          <!-- add field -->
          <el-collapse-transition>
          <li class="list-group-item text-left" v-if="add==index_group">
            <el-form ref="form" :model="cur_field" label-width="100px">
              <el-form-item label="字段名称:">
                <el-input v-model="cur_field.name"></el-input>
              </el-form-item>
              <el-form-item label="字段类型:">
                <el-select v-model="cur_field.type" placeholder="请选择字段类型">
                  <el-option
                    v-for="item in field_types"
                    :key="item.name"
                    :label="item.label"
                    :value="item.name">
                  </el-option>
                </el-select>
                <el-checkbox v-model="cur_field.multiple" class="ml-5" v-show="cur_field.type == 'select' || cur_field.type == 'file'">多选</el-checkbox>
              </el-form-item>
              <el-form-item label="字段默认值:">
                <el-input v-model="cur_field.default"></el-input>
              </el-form-item>

              <el-form-item label="字段可选值:" v-if="cur_field.type == 'select'">
                <el-input :placeholder="'请输入可能值, 以分号分隔'" v-model="cur_field.value"></el-input>
              </el-form-item>
              
              <el-form-item label="附加字段:" v-if="(cur_field.type == 'select') && (cur_field.value)">
                <el-input placeholder="请输入附加字段名(仅支持字符串型子字段)" v-model="cur_field.sub_name" class="input-with-select">
                  <el-select  slot="prepend" placeholder="请选择" v-model="cur_field.sub_key" style="width:120px">
                    <el-option
                      v-for="item in cur_field.value.split(';')"
                      :key="item"
                      :label="item"
                      :value="item">
                    </el-option>
                  </el-select>
                  <el-button slot="append" icon="el-icon-plus" @click="addsub"></el-button>
                </el-input>

                <div class="input-group mt-1" v-for="(sub_item, sub_index) in cur_field.subs" :key="sub_index">
                  <div class="input-group-prepend"><span class="input-group-text">{{ sub_item.key}}</span></div>
                  <input type="text" class="form-control" :placeholder="sub_item.name" disabled>
                </div>
              </el-form-item>

              <el-form-item >
                <el-button type="primary" @click="addfield(index_group)">添加字段</el-button>
              </el-form-item>
            </el-form>
          </li>
          </el-collapse-transition>

          <li class="list-group-item">
            <code>{{ formdata }}</code>
          </li>
          <!-- 渲染后的表单 -->
          <li class="list-group-item text-left" v-for="(field, index) in group.fields" :key="index">
            <div class="form-inline row">
              <label class="mr-1 d-block text-right" style="width:90px">{{ field.label }}:</label>
              <!-- number(int, float) -->
              <input type="number" class="form-control" :name="field.name" :placeholder="'Enter '+field.label" v-model="formdata['group'+index_group+'-'+field.name]" v-if="field.type=='number'" style="width:1%; flex:1 auto">
              
              <!-- select -->
              <div class="card border-0" v-if="field.type=='select'" style="flex: auto">
                <!-- selcet -->
                <el-select v-model="formdata['group'+index_group+'-'+field.name]" :placeholder="'请选择'+field.label" :multiple="field.multiple" v-if="field.type=='select'" style="width:100%; flex:1 auto">
                  <el-option
                    v-for="item in field.values"
                    :key="item.value"
                    :label="item.value"
                    :value="item.value">
                  </el-option>
                </el-select>
                <!-- subs 单选框，选择某个特定项后出现额外填写内容-->
                <div class="w-100 mt-1" v-if="field.type=='select' && !field.multiple ">
                  <!-- 遍历field.values -->
                  <div class="w-100 " v-for="(field_value, field_index) in field.values.filter(field_value => {return field_value.subs && formdata[group.name+'-'+field.name]==field_value.value})" :key="field_index">
                    <!-- 判断并遍历value.subs -->
                    <div class="input-group mt-1"
                      v-for="(sub_value, sub_index) in field_value.subs" :key="sub_index"
                    >
                      <div class="input-group-prepend">
                        <span class="input-group-text">{{ sub_value.label }}</span>
                      </div>
                      <input type="text" :placeholder="'Enter '+sub_value.label" class="form-control" v-model="formdata['group'+index_group+'-'+field.name+'-'+field_value.value+'-'+sub_value.name]">
                    </div>
                  </div>
                  
                </div>
              </div>

              <!-- file -->
              <el-upload
                v-if="field.type=='file'"
                :action="file_upload"
                :multiple="field.multiple"
                :auto-upload="false"
                list-type="picture-card"
                :on-remove="handleRemove"
              >
                <i class="el-icon-plus"></i>
              </el-upload>
              <el-dialog :visible.sync="dialogVisible" v-if="field.type=='file'">
                <img width="100%" :src="dialogImageUrl" alt="">
              </el-dialog>

              <!-- text -->
              <el-input :placeholder="'Enter '+field.label" v-model="formdata['group'+index_group+'-'+field.name]" v-if="field.type=='text'" style="width:1%; flex:1 auto"></el-input>
              <!-- textarea -->
              <el-input type="textarea" :rows="2" :placeholder="'Enter '+field.label" v-model="formdata['group'+index_group+'-'+field.name]" v-if="field.type=='textarea'" style="width:1%; flex:1 auto"></el-input>
              

              <!-- datetime -->
              <el-date-picker
                v-model="formdata['group'+index_group+'-'+field.name]" v-if="field.type=='datetime'" style="width:1%; flex:1 auto"
                type="datetime"
                placeholder="选择日期时间">
              </el-date-picker>
              <!-- <small id="emailHelp" class="form-text text-muted">{{ field }}</small> -->
            </div>
          </li>

        </ul>
        
      </div>
    </div>
  </div>
</template>

<script lang="ts">
// https://github.com/kaorun343/vue-property-decorator`
import { Component, Prop, Vue } from "vue-property-decorator";
import axios from "axios";
import Element from "element-ui";
import "element-ui/lib/theme-chalk/index.css";
Vue.use(Element);

@Component
export default class ClinicalTemplate extends Vue {
  @Prop() private msg!: string;
  // 创建表单 or 渲染表单并上传数据
  @Prop() private editable!: string;
  // 当前模板的配置内容
  @Prop() private template_config!: any;

  // @Watch('person', { immediate: true, deep: true })
  // onPersonChanged1(val: Person, oldVal: Person) { }

  // @Emit(event?: string) decorator

  // 表单支持的类型
  field_types: Array<{ name: string; label: string }> = [
    { name: "number", label: "数字" },
    { name: "text", label: "字符串" },
    { name: "textarea", label: "段落" },
    { name: "file", label: "文件" },
    { name: "datetime", label: "日期时间" },
    { name: "select", label: "选择" }
  ];

  config: any = {};

  // toggle 添加字段模块
  add: number = -1; // 点击添加fields时, add修改为对应组
  // 当前待添加字段的内容
  cur_field: { [key: string]: any } = {};

  // 用户填写的表单实际内容
  formdata: { [key: string]: any } = {};

  file_upload: string = "/";
  fileList: Array<{ name: string; url: string }> = [
    {
      name: "food.jpeg",
      url:
        "https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100"
    },
    {
      name: "food2.jpeg",
      url:
        "https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100"
    }
  ];
  dialogImageUrl: string = "";
  dialogVisible: boolean = false;

  // 添加组
  add_group() {
    if (!this.config["groups"]) this.config["groups"] = [];
    this.formdata["group" + this.config["groups"].length] = {};
    this.config["groups"].push({});
    this.$forceUpdate();
  }

  // 新增或修改表单模板相关函数   select字段在选择某些选项时，需要填写额外内容
  addsub() {
    if (this.cur_field["sub_name"] && this.cur_field["sub_key"]) {
      if (!this.cur_field["subs"]) {
        this.cur_field["subs"] = [];
      }
      this.cur_field["subs"].push({
        name: this.cur_field["sub_name"],
        key: this.cur_field["sub_key"]
      });
      this.cur_field["sub_name"] = "";
      this.cur_field["sub_key"] = "";
    }
  }

  // 新增或修改表单模板相关函数   添加字段
  addfield(index_group: number) {
    let field_item: { [key: string]: any } = {
      name: this.cur_field["name"],
      label: this.cur_field["name"],
      type: this.cur_field["type"],
      default: this.cur_field["default"],
      multiple: this.cur_field["multiple"]
    };
    if (field_item["type"] == "select") {
      let tmpvalue = this.cur_field["value"].split(";");
      // 处理subs
      let tmpobj: any = {};
      this.cur_field["value"].split(";").forEach((i: any) => {
        return (tmpobj[i] = { value: i, subs: [] });
      });
      if (this.cur_field["subs"]) {
        this.cur_field["subs"].forEach((item: any) => {
          tmpobj[item["key"]].subs.push({
            name: item["name"],
            label: item["name"],
            type: "text"
          });
        });
      }
      field_item["values"] = [];
      for (let key in tmpobj) {
        field_item["values"].push(tmpobj[key]);
      }
    }
    // 提取表单内容，生成新的条目，插入到指定的group中
    if (!this.config["groups"][index_group].fields)
      this.config["groups"][index_group].fields = [];
    this.config["groups"][index_group].fields.push(field_item);
    this.cur_field = { subs: [], multiple: false };
  }

  url_prefix: string = "http://localhost:5000/clinicals";
  url_save_template: string = this.url_prefix + "/savetemplate/";
  // 新增或修改表单模板相关函数   保存模板
  save_template() {
    console.log(JSON.stringify(this.config));
    // templateid
    const templateid = this.config.templateid;
    axios
      .post(this.url_save_template + templateid, JSON.stringify(this.config))
      .then((resp: any) => {
        // console.log(resp.data.templateid);
        this.config.templateid = resp.data.templateid;
      });
  }
  // 新增或修改表单模板相关函数   保存组
  save_group() {
    /* 无需操作 */
  }

  // 处理图片上传
  handleRemove(file: object, fileList: Array<object>) {
    console.log(file, fileList);
  }
  handlePreview(file: object) {
    console.log(file);
  }
  handleExceed(files: Array<object>, fileList: Array<object>) {
    this.$message.warning(
      `当前限制选择 3 个文件，本次选择了 ${
        files.length
      } 个文件，共选择了 ${files.length + fileList.length} 个文件`
    );
  }
  beforeRemove(file: any, fileList: Array<object>) {
    return this.$confirm(`确定移除 ${file.name}？`);
  }

  handlePictureCardPreview(file: any) {
    this.dialogImageUrl = file.url;
    this.dialogVisible = true;
  }

  // 组件初始化时，从后端获取模板列表
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
        // TODO 设置默认值
        // const data = {
        //   获取模板失败: {
        //     product: "",
        //     template_name: "获取模板失败",
        //     url: "",
        //     templateid: "#"
        //   }
        // };
        this.template_list = {};
      });
  }

  // 切换模板时，根据url获取模板
  change_template(template_key) {
    // console.log(template_key);
    // config=template_list[cur_template]
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

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="less">
h3 {
  margin: 40px 0 0;
}
</style>
