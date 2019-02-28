<template>
  <b-table bordered  responsive 
    :items="items" 
    :per-page="page['perPage']" 
    :current-page="page['currentPage']"
    :fields="show_fields2"
  >
    <template slot="table-caption">
      <div class="row">
        <p class="d-inline col mt-1 mb-0">Items : {{ items.length }}/{{ total_count }} </p>
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
import * as types from "../stores/mutations_type";

@Component
export default class ClinicalTable extends Vue {
  @Prop() private url!: string;
  // 分组配置信息
  @Prop() private show_fields!: string[];
  @Prop() private page!: any;

  @Watch("url")
  handleUrlChange(url: string, oldUrl: string) {
    if (url) {
      this.init_items();
    }
  }

  items: any[] = [];
  header: string[] = [];
  total_count: number = 0;
  created() {
    this.init_items(true);
  }

  init_items(first: boolean = false) {
    this.$axios.get(this.url).then(({ data }) => {
      if (data.status != "success") {
        this.$notify({
          type: "error",
          title: data.status,
          message: data.msg,
          duration: 10000
        });
        return;
      }
      data = data.data;
      if (data instanceof Array) {
        if (data.length) this.header = Object.keys(data[0]);
        this.items = data;
      } else {
        this.items = [];
        this.$notify({
          type: "error",
          title: "Unknown Data Type",
          message: "Array Data Expeired! But Got " + typeof data
        });
        return;
      }
      if (first) this.total_count = this.items.length;
      this.page.totalRows = this.items.length;
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

  show_detail(row) {
    this.$store.commit(types.SHOW_ITEM, row.item);
    this.$router.push({ path: "/detail" });
  }

  delete_item(row) {
    this.$store
      .dispatch(types.ACTION_DELETE_ITEM, {
        index: row.index,
        id: row.item.id
      })
      .then(rsp => {
        this.$store.commit(types.DEL_ITEMS, row.item.id);
        this.items.splice(row.index, 1);
      });
  }
}
</script>
