<template>
  <div class="container-flex">
    <!-- 统计信息 -->
    <div class="row" v-show="false">
      <div class="card w-25" style="min-height:100px" v-for="(item, index) in 4" :key="index">
        <p>statistics something</p>
      </div>
    </div>

    <!-- <div class="row border-top mt-3"><code> </code></div> -->

    <!-- 搜索栏 and  模板选择 -->
    <div class="row mt-3 my-1">
      <!-- 搜索 -->
      <div class="input-group col-7 pl-0">
        <input type="text" class="form-control" style="height:40px" v-model="query" @blur="search">
        <div class="input-group-append">
          <button class="btn btn-outline-secondary" @click="search">搜索</button>
        </div>
      </div>

      <!-- 选择模板 -->
      <TemplateSwitch v-bind:url="`${$store.state.url_prefix}/templatelist`" class="col-2 " v-on:change_template="handleTemplateChange"/>

      <div class="col-3 input-group px-0">
        <el-button class="el-icon-plus col" @click="$router.push({path:'adddata'})"> 添加数据</el-button>
        <el-button class="el-icon-setting col" @click="$router.push({path:'template'})"> 模板设置</el-button>
      </div>
    </div>

    <!-- 数据展示 -->
    <div class="row table-responsible">
      <div class="input-group my-1" v-if="$store.getters.config.groups">
        <!-- 显示或隐藏列 -->
        <div class="input-group-prepend">
          <p class="input-group-text">显示或隐藏字段</p>
        </div>
        <FieldSelect :groups="group" v-model="show_fields"  class="col-4" />

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
      <ClinicalTable :url="`${$store.state.url_prefix}/data${query_}`" :page="page" :show_fields="show_fields"/>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import TemplateSwitch from "@/components/TemplateSwitch.vue";
import FieldSelect from "@/components/FieldSelect.vue";
import ClinicalTable from "@/components/ClinicalTable.vue";

@Component({
  components: { TemplateSwitch, FieldSelect, ClinicalTable }
})
export default class Index extends Vue {
  page: { [key: string]: number | number[] } = {
    perPage: 10,
    page_select: [10, 20, 50, 100],
    totalRows: 10, // 总数据量
    currentPage: 1 // 当前页码
  };
  group = this.$store.getters.config.groups || [{ fields: [] }];
  show_fields: string[] = this.group[0].fields.map(i => i.name);
  query: string = "";
  query_: string = "";

  handleTemplateChange() {
    this.group = this.$store.getters.config.groups;
    // console.log(this.group);
    if (this.group.length && this.group[0].fields)
      this.show_fields = this.group[0].fields.map(i => i.name);
  }

  search() {
    if (this.query) this.query_ = "?query=" + this.query;
    else this.query_ = "";
  }
}
</script>
