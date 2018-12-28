<template>
  <div class="about">
    <el-container>
      <!-- 筛选区域 -->
      <el-header>
        筛选条件区域
        <el-row :gutter="20">
          <el-col :xs="24" :sm="12">
            <el-input></el-input>
          </el-col>
        </el-row>
      </el-header>
      <!-- 数据展示区 -->
      <el-main>
        <h1>Show All Mutations</h1>
        <!-- 表格数据展示区域 -->
        数据展示
      </el-main>
    </el-container>
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
    fields = {
      basic: ['CHROM', 'POS', 'REF', 'ALT', 'AC', 'DP', 'AF'],
      snpeff: []
    },
    cf = [],
    wbc = null
  },
  methods: {
    
  },
}
</script>