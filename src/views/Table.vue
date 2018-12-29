<template>
  <div class="container-flex">
    <!-- <img src="../assets/logo.png"> -->
    <!-- 筛选区域 -->
    <div class="filter">
      <!-- 筛选条件区域 -->
      <div class="filter-header row">
        <div class="col-sm-8">
          <div class="input-group">
            <input type="text" name="search" class="form-control">
            <a class="btn btn-primary input-group-addon" role="button">Search</a>
          </div>
        </div>
        <div class="col-sm-4">
          <a role="button" class="btn btn-outline-secondary">筛选</a>
          <a role="button" class="btn btn-outline-secondary">导出</a>
          <a role="button" class="btn btn-outline-secondary">上传</a>
        </div>
      </div>
      <div class="filter-new well">
        <!-- 新建过滤条件 -->
        <div class="btn-group">
          <button class="btn btn-default dropdown-toggle" type="button" data-toggle="dropdown">选择数据库来源 <span class="caret"></span></button>
          <ul class="dropdown-menu">
            <li v-for="(db_name, db) in annos" :key="db"><a role="button">db_name</a></li>
          </ul>
        </div>
      </div>
      <table class="table">
        <tr class="table-row filter-item">
          <td><label class="col-sm-1">CHROM:</label></td>
          <td class="col-sm-11">
            <i v-for="chr in chroms_func()" :key="chr" class="btn">{{ 'CHR'+chr }}</i>
          </td>
        </tr>
      </table>
      
    </div>

    <!-- 数据展示区 -->
    <h1>Show All Mutations</h1>
    <!-- 表格数据展示区域 -->
    数据展示
  </div>
</template>

<script>
/**
1. 组件加载后, 读取文件内容, 提取出cf和wbc
2. 渲染出table
2.1. chr, pos, ref, alt, dp, ac, af, annos(snpeff, cosmic, 1000g, dbsnp, ...)
3. 填写刷选条件，过滤不符合的突变
*/
import "../assets/anno"

export default {
  data: () => {
    return {
      annos : {
        basic: ['CHROM', 'POS', 'REF', 'ALT', 'AC', 'DP', 'AF'],
        snpeff: []
      },
      conditions : {
        "CHROM": {'type':'range', 'value':[1,2,3,4,5,6,7,8,9,10,11,12,13,14]}
      },
      cf : [],
      wbc : null
    }
  },
  computed: {
    chroms: () => {
      // var i = 1;
      // while (i < 23){
      //   yield i;
      // }
      // yield x;
      // yield y;
      // return;
      var s = [];
      for(item = 1; item <= 23; item += 1){
        s.push(item);
      }
      s.push(['X','Y','M']);
      return s;
    }
  },
  created: () => {
    axios.get('./assets/anno.json').then(data => {
        this.fields = data
      }).catch(err => {console.log(err)})
  },
  methods: {
    chroms_func: () => {
      // var i = 1;
      // while (i < 23){
      //   yield i;
      // }
      // yield x;
      // yield y;
      // return;
      var s = [];
      for(var item = 1; item <= 23; item += 1){
        s.push(item);
      }
      s.push('X','Y','M');
      return s;
    }
  }
}
</script>

<style lang="less" scoped>
// .filter-item {
//   label {
//     width: 150px;
//     border: 1px solid red;
//     text-align: right;
//   }
//   .item {
//     width: auto;

//   }
// }
</style>
