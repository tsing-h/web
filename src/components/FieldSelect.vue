<template>
  <div class="col mx-0 px-0 ">
    <el-select 
      v-model="selected"  @change="$emit('input', selected)"
      multiple filterable  :collapse-tags="selected.length>3"
      placeholder="请选择"  class="col px-0 mx-0"
    >
      <el-option-group
        v-for="group in fields"
        :key="group.name"
        :label="group.label">
        <el-option
          v-for="item in group.options"
          :key="item.value"
          :label="item.value"
          :value="item.value">
        </el-option>
      </el-option-group>
    </el-select>
    <!-- <code>{{ fields }}</code> -->
  </div>
</template>

<script lang="ts">
import { Component, Prop, Watch, Model, Vue } from "vue-property-decorator";
import axios from "axios";

@Component
export default class FieldSelect extends Vue {
  //
  // @Prop() private url!: string;
  // 分组配置信息
  @Prop() private groups!: Array<any>;

  // 组件数据交互 v-model功能需要有个Prop：value，以及适当情况下$emit("input", value)
  @Prop() private value!: { [key: string]: any };
  // @Model("change", {type: string[]}) value!: string[];

  @Watch("groups")
  onConfigChanged(val: any, oldVal: any) {
    this.selected = [];
  }

  selected: string[] = [];

  public get fields(): Array<any> {
    let items: any[] = [];
    this.groups.forEach(element => {
      // console.log(element);
      let options: any[] = [];
      element.fields.forEach(field => {
        options.push({ label: field.name, value: field.name });
      });
      items.push({ name: element.name, label: element.name, options });
    });
    return items;
  }
}
</script>
