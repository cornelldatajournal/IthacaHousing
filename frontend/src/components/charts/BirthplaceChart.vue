<template>
    <div>
      <h2>Birthplace Origins of Ithaca Residents</h2>
      <div ref="chart" style="width: 100%; height: 500px;"></div>
    </div>
  </template>
  
  <script>
import Plotly from 'plotly.js-dist';
  
  export default {
    name: 'BirthplaceChart',
    mounted() {
      const labels = [
        'Born in NY, Parents Born in NY',
        'Born in NY, Parents NOT Born in NY',
        'Born in US, NOT NY',
        'Born Outside US'
      ];
      const colors = ['#f8b195', '#f67280', '#c06c84', '#6c5b7b'];
  
      const values1920 = [50.1, 24.9, 14.7, 10.3];
      const values1930 = [43, 26.7, 19.9, 10.4];
  
      const data = [
        {
          type: 'pie',
          labels,
          values: values1920,
          marker: { colors },
          domain: { column: 0 },
          name: '1920',
          hoverinfo: 'label+percent+name',
          textinfo: 'label+percent'
        },
        {
          type: 'pie',
          labels,
          values: values1930,
          marker: { colors },
          domain: { column: 1 },
          name: '1930',
          hoverinfo: 'label+percent+name',
          textinfo: 'label+percent'
        }
      ];
  
      const layout = {
        title: 'Birthplace Comparison: 1920 vs 1930',
        grid: { rows: 1, columns: 2 },
        showlegend: true
      };
  
      Plotly.newPlot(this.$refs.chart, data, layout);
    }
  };
  </script>
  
  <style scoped>
  h2 {
    font-family: 'Inter', sans-serif;
    font-weight: 600;
    margin-bottom: 10px;
  }
  </style>
  