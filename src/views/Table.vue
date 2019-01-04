<template>
  <div class="container-flex">
    <!-- <img src="../assets/logo.png"> -->
    <!-- 筛选区域 -->
    <div class="filter">
      <!-- 筛选条件区域 -->
      <div class="filter-header no-gutters row pb-2">
        <div class="col-7">
          <div class="input-group">
            <input type="text" name="search" class="form-control">
            <a class="btn btn-outline-secondary input-group-addon" role="button">Search</a>
          </div>
        </div>
        <div class="col-5 row no-gutters">
          <a role="button" class="btn btn-outline-secondary col ml-3" data-toggle="collapse" data-target="#filter">筛选</a>
          <a role="button" class="btn btn-outline-secondary col ml-3">导出</a>
          <a role="button" class="btn btn-outline-secondary col ml-3">上传</a>
        </div>
      </div>

      <!-- input-group 三级选择框 -->
      <div id="filter" class="input-group mt-3" v-if="fields">
        <select
          class="custom-select col"
          v-model="local_vals['selected_db']"
          @change="local_vals['selected_field']=0"
        >
          <option selected value="0">选择数据库来源</option>
          <option v-for="(db, db_name) in fields" :key="db_name" :value="db_name">{{ db_name }}</option>
        </select>
        
        <select
          class="custom-select col"
          v-model="local_vals['selected_field']"
          @change="local_vals['selected_type']=0"
          v-if="local_vals['selected_db'] && local_vals['selected_db'] !='0'"
        >
          <option selected value="0">选择字段</option>
          <option
            v-for="cur_fields in fields[local_vals['selected_db']]['fields']"
            :key="cur_fields[0]"
            :value="cur_fields[0]"
          >{{ cur_fields[0] }}</option>
        </select>
        
        <select
          class="custom-select col"
          v-model="local_vals['selected_type']"
        >
          <option selected value="0">选择过滤类型</option>
          <option
            v-for="field_type in conditions['type']"
            :key="field_type"
            :value="field_type"
          >{{ field_type }}</option>
        </select>
      </div>

      <!-- 范围型字段条件 -->
      <div class="input-group mt-1">
        <div class="input-group-prepend">
          <a href="#" class="btn btn-outline-secondary">Range:</a>
        </div>
        <input type="text" class="form-control">
        <div class="input-group-append">
          <span class="input-group-text">~</span>
        </div>
        <input type="text" class="form-control">
        <div class="input-group-append">
          <a href="#" class="btn btn-dark">Add</a>
        </div>
      </div>
      
      <!-- 离散型字段 -->
      <div class="input-group mt-1">
        <div class="input-group-prepend">
          <a href="#" class="btn btn-outline-secondary">离散值:</a>
          <p class="input-group-text" v-for="item in chroms" :key="item">{{ item }}</p>
        </div>
        <input type="text" class="form-control" placeholder="add new value">
        <div class="input-group-append ml-auto">
          <a href="#" class="btn btn-dark">Add</a>
        </div>
      </div>

      <table class="table">
        <tr class="table-row filter-item">
          <td>
            <label class="col-sm-1">CHROM:</label>
          </td>
          <td class="col-sm-11">
            <i v-for="chr in chroms" :key="chr" class="btn">{{ 'CHR'+chr }}</i>
          </td>
        </tr>
      </table>
    </div>

    <!-- 数据展示区 -->
    <!-- 表格数据展示区域 -->
    <div class="table-responsiable">
      <div class="input-group my-1">
        <div class="input-group-prepend">
          <!-- <a href="#" class="btn btn-outline-secondary">选择默认显示字段:</a> -->
          <p class="input-group-text">显示或隐藏字段</p>
        </div>

        <el-select v-model="show_fields" multiple placeholder="请选择" collapse-tags >
          <el-option-group
            v-for="(group, db_name) in fields"
            :key="db_name"
            :label="db_name">
            <el-option
              v-for="item in group.fields"
              :key="item[0]"
              :label="item[0]"
              :value="item[0]">
            </el-option>
          </el-option-group>
        </el-select>
      </div>

      <table class="table table-dark table-striped">
        <caption>Total Mutations {{ 10 }}</caption>
        <thead>
          <tr>
            <td scope="col" style>#</td>
            <td scope="col" v-for="field in show_fields" :key="field">{{ field }}</td>
            <td scope="col" style>Actions</td>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(item, index) in items" :key="index">
            <td>{{ index + 1 }}</td>
            <td v-for="field in show_fields" :key="field">{{ item[field] }}</td>
            <td>
              <div class="btn-group" role="group">
                <a href="#" class="btn btn-sm btn-secondary mr-2">加入报告</a>
                <a href="#" class="btn btn-sm btn-secondary">详细信息</a>  
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
// 1. 组件加载后, 读取文件内容, 提取出cf和wbc
// 2. 渲染出table
// 2.1. chr, pos, ref, alt, dp, ac, af, annos(snpeff, cosmic, 1000g, dbsnp, ...)
// 3. 填写刷选条件，过滤不符合的突变

import "../assets/anno";

export default {
  data: () => {
    return {
      annos: {
        basic: ["CHROM", "POS", "REF", "ALT", "AC", "DP", "AF"],
        snpeff: ["HGVS-P", "HGVS-C"],
        cosmic: ["cnt-breast", "cnt-lung"],
        "1000genome": ["all", "afr", "amr"]
      },
      conditions: {
        type: ["离散值", "数值范围", "相似"]
      },
      show_fields: ["CHROM", "POS", "REF", "ALT", "AC", "DP", "AF"],
      cf: [],
      wbc: null,
      items: [
        {
          CHROM: 1,
          POS: 1000,
          REF: "A",
          ALT: "AG",
          AC: 1,
          DP: 555,
          AF: ((1 / 555) * 100).toFixed(3) + "%"
        },
        {
          CHROM: 1,
          POS: 1000,
          REF: "A",
          ALT: "AG",
          AC: 1,
          DP: 555,
          AF: ((1 / 555) * 100).toFixed(3) + "%"
        },
        {
          CHROM: 1,
          POS: 1000,
          REF: "A",
          ALT: "AG",
          AC: 1,
          DP: 555,
          AF: ((1 / 555) * 100).toFixed(3) + "%"
        },
        {
          CHROM: 1,
          POS: 1000,
          REF: "A",
          ALT: "AG",
          AC: 1,
          DP: 555,
          AF: ((1 / 555) * 100).toFixed(3) + "%"
        },
        {
          CHROM: 1,
          POS: 1000,
          REF: "A",
          ALT: "AG",
          AC: 1,
          DP: 555,
          AF: ((1 / 555) * 100).toFixed(3) + "%"
        }
      ],
      fields: {},
      // 一些局部变量
      local_vals: {
        selected_db: 0,
        selected_field: 0,
        selected_type: 0,
        selected_value: { type: null, from: 0, to: 0, values: [] },
        selected_condition: ''
      }
    };
  },
  computed: {
    chroms: () => {
      const s = [];
      for (let item = 1; item <= 23; item += 1) {
        s.push(item);
      }
      s.push("X", "Y", "M");
      return s;
    },
    allfields: function() {
      return {}
    },
    items4ele: function () {
      // return this;
      // 将数据转换为ele 级联选择器适用的数据格式
      let a = [];
      for (let i in this.annos) {
        let tmp = {value:i, label:i};
        tmp['options'] = []
        for (let j in this.annos[i]) {
          tmp['options'].push({value:this.annos[i][j], label:this.annos[i][j]});
        }
        a.push(tmp);
      }
      return a;
    },
    items4ele2: function () {
      // return this;
      // 将数据转换为ele 级联选择器适用的数据格式
      let a = [];
      for (let i in this.annos) {
        let tmp = {value:i, label:i};
        tmp['children'] = []
        for (let j in this.annos[i]) {
          tmp['children'].push({value:this.annos[i][j], label:this.annos[i][j]});
        }
        a.push(tmp);
      }
      return a;
    }
  },
  created: function() {
    let _this = this;
    // early-screen2\src\assets\anno.json
    axios.get('/anno.json').then(data => {
        // console.log(this)
        _this.fields = data.data[0]
        // show_fields = this.fields['basic']
      }).catch(err => {console.log(err)});
    
    axios.get('/cf.tsv').then(data => {
      _this.wbc = data.data
    });

    console.log('created');
  },
  methods: {
    chroms_func: () => {
      const s = [];
      for (let item = 1; item <= 23; item += 1) {
        s.push(item);
      }
      s.push("X", "Y", "M");
      return s;
    },
    convert: (item) => {
      return {value: item, lable: item};
    }
  }
};
</script>

<style lang="less" scoped>
// .filter {
// .filter-header {
// }
// .filter-new {
// }
// }
.border-red {
  border: 1px solid red;
}
</style>
