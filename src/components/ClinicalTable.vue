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
  <!-- 
    <template slot="chr_pos" slot-scope="row">
      {{ row.item.chrom }}-{{ row.item.pos }}-{{ row.item.ref }}-{{ row.item.alt }}
    </template>
    <template slot="wbc" slot-scope="row">
      {{ row.item.wbc  }}
    </template>
    <template slot="af" slot-scope="row">
      {{ (parseFloat(row.item.af)*100).toFixed(2) + "%"  }} 
    </template>
    -->
    <template slot="ACTIONS" slot-scope="row">
        <b-button size="sm" @click.stop="$router.push({path:'/detail', params: row})"> Details</b-button>
    </template>
    <!--
    Details
    <template slot="row-details" slot-scope="row" >
      <div class="card">
        <table class="table table-sm table-bordered" v-for="(db_info, db_name) in fields" :key="db_name">
          <tr   >
            <td rowspan="2" style="vertical-align: middle; width:7rem; " class="br-1">{{ db_name }}</td>
            <td v-for="(item, index) in db_info.fields" :key="index">
              <div class="badge text-truncate" style=" flex:1 auto" :title="item[0].toLowerCase()">
                {{ item[0].toLowerCase() }}
              </div>
            </td>
          </tr>
          <tr  >
            <td class="" v-for="(item, index) in db_info.fields" :key="index">
              <div class="badge  text-truncate" style=" flex:1 auto" :title="row.item[item[0].toLowerCase()]">
                {{ row.item[item[0].toLowerCase()] }}
              </div>
            </td>
          </tr>
        </table>
      </div>
    </template>
    -->
  </b-table> 
  <!-- <div class="card">
    <code>{{ items }}</code>
  </div> -->
</template>

<script lang="ts">
import { Component, Prop, Watch, Model, Vue } from "vue-property-decorator";
import axios from "axios";

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

  items: any[] = [];
  header: string[] = [];
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
