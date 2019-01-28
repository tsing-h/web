<template>
  <el-form ref="form" :model="field" label-width="100px">
    <el-form-item label="字段名称:">
      <el-input v-model="field.name"></el-input>
    </el-form-item>
    <el-form-item label="字段类型:">
      <el-select v-model="field.type" placeholder="请选择字段类型">
        <el-option
          v-for="item in field_types"
          :key="item.name"
          :label="item.label"
          :value="item.name">
        </el-option>
      </el-select>
      <el-checkbox v-model="field.multiple" class="ml-5" v-show="field.type == 'select' || field.type == 'file'">多选</el-checkbox>
    </el-form-item>
    <el-form-item label="字段默认值:">
      <el-input v-model="field.default"></el-input>
    </el-form-item>

    <el-form-item label="字段可选值:" v-if="field.type == 'select'">
      <el-input :placeholder="'请输入可能值, 以分号分隔'" v-model="field.value"></el-input>
    </el-form-item>
    
    <el-form-item label="附加字段:" v-if="(field.type == 'select') && (field.value)">
      <el-input placeholder="请输入附加字段名(仅支持字符串型子字段)" v-model="field.sub_name" class="input-with-select">
        <el-select  slot="prepend" placeholder="请选择" v-model="field.sub_key" style="width:120px">
          <el-option
            v-for="item in field.value.split(';')"
            :key="item"
            :label="item"
            :value="item">
          </el-option>
        </el-select>
        <el-button slot="append" icon="el-icon-plus" @click="addsub"></el-button>
      </el-input>

      <div class="input-group mt-1" v-for="(sub_item, sub_index) in field.subs" :key="sub_index">
        <div class="input-group-prepend"><span class="input-group-text">{{ sub_item.key}}</span></div>
        <input type="text" class="form-control" :placeholder="sub_item.name" disabled>
      </div>
    </el-form-item>

    <el-form-item >
      <el-button type="primary" @click="addfield()">添加字段</el-button>
    </el-form-item>
  </el-form>
</template>

<script lang="ts">
import { Component, Prop, Model, Emit, Vue } from "vue-property-decorator";

@Component
export default class FieldGenerate extends Vue {
  // @Prop() private field!: { [key: string]: any };
  // @Prop() private edit!: boolean;

  @Model("submit", { type: Object })
  field!: { [key: string]: any };

  // 表单支持的类型
  field_types: Array<{ name: string; label: string }> = [
    { name: "number", label: "数字" },
    { name: "text", label: "字符串" },
    { name: "textarea", label: "段落" },
    { name: "file", label: "文件" },
    { name: "datetime", label: "日期时间" },
    { name: "select", label: "选择" }
  ];
  // 新增或修改表单模板相关函数   select字段在选择某些选项时，需要填写额外内容
  addsub() {
    if (this.field["sub_name"] && this.field["sub_key"]) {
      if (!this.field["subs"]) {
        this.field["subs"] = [];
      }
      this.field["subs"].push({
        name: this.field["sub_name"],
        key: this.field["sub_key"]
      });
      this.field["sub_name"] = "";
      this.field["sub_key"] = "";
    }
  }

  // 新增或修改表单模板相关函数   添加字段
  @Emit("submit")
  addfield() {
    let field_item: { [key: string]: any } = {
      name: this.field["name"],
      label: this.field["name"],
      type: this.field["type"],
      default: this.field["default"],
      multiple: this.field["multiple"]
    };
    if (field_item["type"] == "select") {
      let tmpvalue = this.field["value"].split(";");
      // 处理subs
      let tmpobj: any = {};
      this.field["value"].split(";").forEach((i: any) => {
        return (tmpobj[i] = { value: i, subs: [] });
      });
      if (this.field["subs"]) {
        this.field["subs"].forEach((item: any) => {
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

    // 将组件数据交给父组件
    this.field = { subs: [], multiple: false };
    // this.field = field_item;
    return field_item;
  }
}
</script>
