<template>
  <div class="row table-responsible">
      <div class="input-group my-1" v-if="$store.getters.config.groups">
        <!-- 显示或隐藏列 -->
        <div class="input-group-prepend">
          <p class="input-group-text">显示或隐藏字段</p>
        </div>
        <FieldSelect :groups="$store.getters.config.groups" v-model="show_fields"  class="col-4" />

        <!-- 设置每页显示行数 -->
        <el-select v-model="page['perPage']" placeholder="每页行数" collapse-tags style="" class="ml-auto">
          <el-option
            v-for="item in page.page_select"
            :key="item"
            :label="item"
            :value="item">
          </el-option>
        </el-select>
        <div class="input-group-append">
          <p class="input-group-text">每页行数</p>
        </div> 
      </div>

      <!-- table -->
      <b-table bordered  responsive 
        :items="items" 
        :per-page="page['perPage']" 
        :current-page="page['currentPage']"
        :fields="show_fields2"
      >
        <template slot="table-caption">
          <div class="row">
            <p class="d-inline col mt-1 mb-0">Mutations : {{ page.totalRows }}/{{ items.length }} </p>
            <b-pagination class="col mb-0" align="right" :total-rows="page.totalRows" v-model="page['currentPage']" :per-page="page['perPage']"></b-pagination>
          </div>
        </template>
      
        <template slot="ACTIONS" slot-scope="row">
            <b-button size="sm" @click.stop="show_detail(row)"> Details</b-button>
        </template>
      </b-table>
    </div>
</template>

<script lang="ts">
import { Component, Prop, Watch, Model, Vue } from "vue-property-decorator";
import axios from "axios";
import * as types from "../stores/mutations_type";
import FieldSelect from "@/components/FieldSelect.vue";

@Component({ components: { FieldSelect } })
export default class ClinicalTable extends Vue {
  //
  @Prop() private url!: string;
  // @Prop() private page!: any;
  // 组件数据交互 v-model功能需要有个Prop：value，以及适当情况下$emit("input", value)
  @Prop() private value!: { [key: string]: any };

  items: any[] = [];
  show_fields: string[] = [];
  header: string[] = [];
  page: { [key: string]: number | number[] } = {
    perPage: 10,
    page_select: [10, 20, 50, 100],
    totalRows: 10, // 总数据量
    currentPage: 1 // 当前页码
  };
  created() {
    axios.get(this.url).then(rsp => {
      // console.log(rsp);
      this.items = this.text2obj(rsp.data);
      this.page.totalRows = this.items.length;
    });
  }

  public get show_fields2(): string[] {
    const action: string = "ACTIONS";
    if (this.show_fields.length == 0) {
      return [...this.header.slice(0, 5), action];
    }
    if (action in this.show_fields) {
      return this.show_fields;
    }
    return [...this.show_fields, action];
  }

  // 一些工具函数
  text2obj(text: string) {
    const data: any[] = [];
    const data2 = {};
    const lines: string[] = this.strim(text).split("\n");
    if (lines.length == 0) return data;

    // 提取表头
    // let header: string[] = [];
    let line = lines.shift();
    if (line) this.header = line.split(",");

    // 处理表格数据
    for (let str_lin of lines) {
      let line: string[] = this.strim(str_lin).split(",");

      const obj: any = {};
      line.forEach((item, index) => {
        // 尝试解析区分数字和字符串
        obj[this.header[index]] = this.parse(item);
      });

      // 附加处理
      // const _key = [obj.chrom, obj.pos, obj.ref, obj.alt].join("-");
      // obj["_key"] = _key;
      data.push(obj);
    }
    return data;
  }

  strim(str: string): string {
    return str.replace(/^\s\s*/, "").replace(/\s\s*$/, "");
  }
  parse(str): string | number {
    if (str.match(/^[+-]?\d+$/)) {
      return parseInt(str);
    }
    if (str.match(/^[-+]?\d+\.\d+$/)) {
      return parseFloat(str);
    }
    if (str.match(/^[-+]?\d+\.\d+%$/)) {
      return parseFloat(str) / 100;
    }

    return str;
  }
  compare(a, b) {
    // return b-a;
    return isFinite(a)
      ? isFinite(b)
        ? a - b
        : -1
      : isFinite(b)
        ? 1
        : a.localeCompare(b);
  }

  show_detail(row) {
    this.$store.commit(types.SHOW_ITEM, row.item);
    this.$router.push({ path: "/detail" });
  }
}
</script>

<style lang="less" scoped>
b-table {
  tbody {
    tr {
      height: 49px;
    }
  }
}
</style>
