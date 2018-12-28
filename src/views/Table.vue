<template>
  <div class="container-flex">
    <!-- 筛选区域 -->
    <div class="well filter">
      <!-- 筛选条件区域 -->
      <div class="alert alert-primary" role="alert">
        This is a primary alert—check it out!
      </div>
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
export default {
  data: () => {
    return {
      fields : {
        basic: ['CHROM', 'POS', 'REF', 'ALT', 'AC', 'DP', 'AF'],
        snpeff: []
      },
      conditions : {

      },
      cf : [],
      wbc : null
    }
  },
  methods: {
    created: () => {
      // 读取本地文件，初始化数据
    }
  },
}
</script>