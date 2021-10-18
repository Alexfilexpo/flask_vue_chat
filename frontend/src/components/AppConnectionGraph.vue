<template>
  <div class="graph-view col-md-6" style="
    background-image: url(https://www.amcharts.com/wp-content/uploads/2013/12/demo_910_none-1.png);
    background-size: 110%;
    background-position: center;
  ">
    <svg width="560" height="360"></svg>
  </div>
</template>
<script>
import * as d3 from 'd3'
export default {
  data () {
    return {}
  },
  mounted () {
    let svg = d3.select('svg')
    let width = svg.attr('width')
    let height = svg.attr('height')
    let g = svg.append('g')

    // Node Dataset
    let nodes = [
      { name: 'Tom' },
      { name: 'Mary' },
      { name: 'Reiner' },
      { name: 'Mika' },
      { name: 'Lessie' },
      { name: 'Alex' },
      { name: 'Tanya' },
      { name: 'Bob' },
      { name: 'Nick' },
      { name: 'Mark' },
    ]

    // Side Dataset
    let edges = [
      { source: 0, target: 1, value: Math.floor(Math.random()+1) },
      { source: 2, target: 3, value: Math.floor(Math.random()+1) },
      { source: 4, target: 5, value: Math.floor(Math.random()+1) },
      { source: 6, target: 7, value: Math.floor(Math.random()+1) },
      { source: 8, target: 9, value: Math.floor(Math.random()+1) },
    ]

    // Set a color scale
    let colorScale = d3.scaleOrdinal()
      .domain(d3.range(nodes.length))
      .range(d3.schemeCategory10)

    // Create a new force guide diagram
    let forceSimulation = d3.forceSimulation()
      .force('link', d3.forceLink())
      .force('charge', d3.forceManyBody())
      .force('center', d3.forceCenter())

    // Generate node data
    forceSimulation.nodes(nodes)
      .on('tick', ticked)

    // Generate side data
    forceSimulation.force('link')
      .links(edges)
      .distance(function (d) { // side length
        return d.value * 250
      })

    // Set drawing center location
    forceSimulation.force('center')
      .x(width / 2)
      .y(height / 2)

    // Draw side
    let links = g.append('g')
      .selectAll('line')
      .data(edges)
      .enter()
      .append('line')
      .attr('stroke', function (d, i) {
        return colorScale(i)
      })
      .attr('stroke-width', 9)

    // Create group
    let gs = g.selectAll('.circleText')
      .data(nodes)
      .enter()
      .append('g')
      .attr('transform', function (d) {
        let cirX = d.x
        let cirY = d.y
        return 'translate(' + cirX + ',' + cirY + ')'
      })

    // Draw node
    gs.append('circle')
      .attr('r', 10)
      .attr('fill', 'white')
      .attr('stroke', function (d, i) {
        return colorScale(i)
      })
      .attr('stroke-width', 6)


    // Draw text
    gs.append('text')
      .attr('x', 10)
      .attr('y', 20)
      .attr('dy', 10)
      .text(function (d) {
        return d.name
      })

    // ticked
    function ticked () {
      links
        .attr('x1', function (d) { return d.source.x })
        .attr('y1', function (d) { return d.source.y })
        .attr('x2', function (d) { return d.target.x })
        .attr('y2', function (d) { return d.target.y })
      gs
        .attr('transform', function (d) { return 'translate(' + d.x + ',' + d.y + ')' })
    }

    // drag
    function started (d) {
      if (!d3.event.active) {
        forceSimulation.alphaTarget(0.8).restart() // Set the attenuation coefficient to simulate the node position movement process. The higher the value, the faster the movement. The value range is [0, 1] // 设置衰减系数，对节点位置移动过程的模拟，数值越高移动越快，数值范围[0, 1]
      }
      d.fx = d.x
      d.fy = d.y
    }
    function dragged (d) {
      d.fx = d3.event.x
      d.fy = d3.event.y
    }
    function ended (d) {
      if (!d3.event.active) {
        forceSimulation.alphaTarget(0)
      }
      d.fx = null
      d.fy = null
    }
  }
}
</script>
<style scoped>
</style>