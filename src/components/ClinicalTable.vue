<template>
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
        <el-button-group>
          <el-button size="mini" round icon="el-icon-view" title="show detail" @click.stop="show_detail(row)"></el-button>
          <el-button size="mini" round icon="el-icon-delete" @click.stop="delete_item(row)"></el-button>
        </el-button-group>
    </template>
  </b-table> 
  
</template>

<script lang="ts">
import { Component, Prop, Watch, Model, Vue } from "vue-property-decorator";
import axios from "axios";
import * as types from "../stores/mutations_type";

@Component
export default class ClinicalTable extends Vue {
  //
  @Prop() private url!: string;
  // 分组配置信息
  @Prop() private show_fields!: string[];
  // @Prop() private items!: Array<any>;
  @Prop() private page!: any;
  // 组件数据交互 v-model功能需要有个Prop：value，以及适当情况下$emit("input", value)
  @Prop() private value!: { [key: string]: any };

  @Watch("url")
  handleUrlChange(url: string, oldUrl: string) {
    if (url) {
      this.init_items();
    }
  }

  items: any[] = [];
  header: string[] = [];
  created() {
    this.init_items();
  }

  init_items() {
    axios.get(this.url).then(({ data }) => {
      // console.log(rsp);
      if (data.status != "success") {
        this.$notify({
          type: "error",
          message: data.msg,
          duration: 10000
        });
        return;
      }
      data = data.data;
      if (data instanceof Array) {
        this.header = Object.keys(data[0]);
        this.page.totalRows = data.length;
        this.items = data;
      } else {
        this.items = this.text2obj(data);
        this.page.totalRows = this.items.length;
      }
      this.$store.commit(types.INIT_ITEMS, this.items);
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

  delete_item(row) {
    // this.$notify.success(JSON.stringify(row.index));
    // this.dispatch()
    this.$store
      .dispatch(types.ACTION_DELETE_ITEM, {
        index: row.index,
        id: row.item.id
      })
      .then(rsp => {
        this.$store.commit(types.DEL_ITEMS, row.item.id);
        this.items.splice(row.index, 1);
        // this.$notify.success("data has been deleted");
      });
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
