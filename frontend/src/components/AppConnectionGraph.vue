<template>
  <div class="graph-view col-md-6" style="
    background-image: url(https://www.amcharts.com/wp-content/uploads/2013/12/demo_910_none-1.png);
    background-size: 110%;
    background-position: center;
  ">
    <svg width="560" height="360"></svg>
    <button type="submit" @submit.prevent @click="getNode">TOUCH ME</button>
  </div>
</template>
<script>
import * as d3 from 'd3'

export default {
  props: ['activeUsersList'],
  data () {
    return {}
  },
  methods: {
    validateData() {
      let userList = this.activeUsersList
      let svg = d3.select("svg"),
          width = +svg.attr("width"),
          height = +svg.attr("height"),
          color = d3.scaleOrdinal()
            .domain(d3.range(this.activeUsersList.length))
            .range(d3.schemeCategory10)

      let nodes = this.activeUsersList,
          links = [];

      let simulation = d3.forceSimulation(nodes)
          .force("charge", d3.forceManyBody().strength(-1000))
          .force("link", d3.forceLink(links).distance(200))
          .force("x", d3.forceX())
          .force("y", d3.forceY())
          .alphaTarget(1)
          .on("tick", ticked);

      let g = svg.append("g")
              .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")")

      let link = g.append("g")
          .attr("stroke", "#000")
          .attr("stroke-width", 1.5)
          .selectAll(".link")

      let node = g.append("g")
          .attr("stroke", "#000")
          .selectAll(".node");

      restart();

      // if (userList.length > 1) {
      //   for (let i = 0; i < userList.length; i++) {
      //     let start = i
      //     let end = ++i
      //     links.push({
      //       source: userList[start],
      //       target: userList[end],
      //       value: Math.floor(Math.random()+1)
      //     })
      //     console.log(links)
      //   }
      // }

      // d3.timeout(function() {
      //   for (let i = 0; i < userList.length; i++) {
      //     let start = i
      //     let end = ++i
      //     links.push({
      //       source: userList[start],
      //       target: userList[end],
      //       value: Math.floor(Math.random()+1)
      //     });
      //   };
      //   // links.push({source: userList[0], target: userList[1]}); // Add a-b.
      //   // links.push({source: userList[1], target: userList[2]}); // Add b-c.
      //   // links.push({source: userList[2], target: userList[3]}); // Add c-a.
      //   restart();
      // }, 1000);

      //
      // d3.interval(function() {
      //   nodes.pop(); // Remove c.
      //   links.pop(); // Remove c-a.
      //   links.pop(); // Remove b-c.
      //   restart();
      // }, 2000, d3.now());
      //
      // d3.interval(function() {
      //   nodes.push(c); // Re-add c.
      //   links.push({source: b, target: c}); // Re-add b-c.
      //   links.push({source: c, target: a}); // Re-add c-a.
      //   restart();
      // }, 2000, d3.now() + 1000);

      function restart() {

        // Apply the general update pattern to the nodes.
        node = node.data(nodes, function(d) { return d.id;});
        node.exit().remove();
        node = node.enter().append("g")
        node.append("circle")
            .attr("stroke", "white")
            .attr("stroke-width", 1.5)
            .attr("fill", function (d, i) {return color(i)})
            .attr("r", 10);
        node.append("text")
            .attr('x', 10)
            .attr('y', 20)
            .attr('dy', 10)
            .text(function (d) {return d.id});

        // Apply the general update pattern to the links.
        link = link.data(links, function(d) { return d.source.id + "-" + d.target.id; });
        link.exit().remove();
        link = link.enter().append("line").merge(link);

        // Update and restart the simulation.
        simulation.nodes(nodes);
        simulation.force("link").links(links);
        simulation.alpha(1).restart();
      }

      function ticked() {
        node.attr('transform', function (d) { return 'translate(' + d.x + ',' + d.y + ')' })

        link.attr("x1", function(d) { return d.source.x; })
            .attr("y1", function(d) { return d.source.y; })
            .attr("x2", function(d) { return d.target.x; })
            .attr("y2", function(d) { return d.target.y; });
      }
    },
    // createGraph() {
    //   let svg = d3.select('svg')
    //   let width = svg.attr('width')
    //   let height = svg.attr('height')
    //   let g = svg.append('g')
    //
    //   let nodes = this.userNodes;
    //
    //   // Side Dataset
    //   // let edges = [
    //   //   { source: 0, target: 1, value: Math.floor(Math.random()+1) },
    //   //   { source: 2, target: 3, value: Math.floor(Math.random()+1) },
    //   //   { source: 4, target: 5, value: Math.floor(Math.random()+1) },
    //   //   { source: 6, target: 7, value: Math.floor(Math.random()+1) },
    //   //   { source: 8, target: 9, value: Math.floor(Math.random()+1) },
    //   // ]
    //   let edges = []
    //   if (nodes.length > 1) {
    //     for (let i = 0; i < nodes.length; i++) {
    //       let start = i
    //       let end = ++i
    //       edges.push({
    //         source: start,
    //         target: end,
    //         value: Math.floor(Math.random()+1)
    //       })
    //     }
    //   }
    //
    //   // Set a color scale
    //   let colorScale = d3.scaleOrdinal()
    //     .domain(d3.range(nodes.length))
    //     .range(d3.schemeCategory10)
    //
    //   // Create a new force guide diagram
    //   let forceSimulation = d3.forceSimulation()
    //     .force('link', d3.forceLink())
    //     .force('charge', d3.forceManyBody())
    //     .force('center', d3.forceCenter())
    //
    //   // Generate node data
    //   forceSimulation.nodes(nodes)
    //     .on('tick', ticked)
    //
    //   // Generate side data
    //   forceSimulation.force('link')
    //     .links(edges)
    //     .distance(function (d) { // side length
    //       return d.value * 250
    //     })
    //
    //   // Set drawing center location
    //   forceSimulation.force('center')
    //     .x(width / 2)
    //     .y(height / 2)
    //
    //   // Draw side
    //   let links = g.append('g')
    //     .selectAll('line')
    //     .data(edges)
    //     .enter()
    //     .append('line')
    //     .attr('stroke', function (d, i) {
    //       return colorScale(i)
    //     })
    //     .attr('stroke-width', 9)
    //     .attr('connection', function (d) {
    //       return d.source.name + '-' + d.target.name
    //     })
    //
    //   // Create group
    //   let gs = g.selectAll('.circleText')
    //     .data(nodes)
    //     .enter()
    //     .append('g')
    //     .attr('transform', function (d) {
    //       console.log(d.id)
    //       let cirX = d.x
    //       let cirY = d.y
    //       return 'translate(' + cirX + ',' + cirY + ')'
    //     })
    //
    //   // Draw node
    //   gs.append('circle')
    //     .attr('r', 10)
    //     .attr('fill', 'white')
    //     .attr('stroke', function (d, i) {
    //       return colorScale(i)
    //     })
    //     .attr('stroke-width', 6)
    //
    //
    //   // Draw text
    //   gs.append('text')
    //     .attr('x', 10)
    //     .attr('y', 20)
    //     .attr('dy', 10)
    //     .text(function (d) {
    //       return d.name
    //     })
    //
    //   // ticked
    //   function ticked () {
    //     links
    //       .attr('x1', function (d) { return d.source.x })
    //       .attr('y1', function (d) { return d.source.y })
    //       .attr('x2', function (d) { return d.target.x })
    //       .attr('y2', function (d) { return d.target.y })
    //     gs
    //       .attr('transform', function (d) { return 'translate(' + d.x + ',' + d.y + ')' })
    //   }
    //
    //   // drag
    //   function started (d) {
    //     if (!d3.event.active) {
    //       forceSimulation.alphaTarget(0.8).restart() // Set the attenuation coefficient to simulate the node position movement process. The higher the value, the faster the movement. The value range is [0, 1] // 设置衰减系数，对节点位置移动过程的模拟，数值越高移动越快，数值范围[0, 1]
    //     }
    //     d.fx = d.x
    //     d.fy = d.y
    //   }
    //   function dragged (d) {
    //     d.fx = d3.event.x
    //     d.fy = d3.event.y
    //   }
    //   function ended (d) {
    //     if (!d3.event.active) {
    //       forceSimulation.alphaTarget(0)
    //     }
    //     d.fx = null
    //     d.fy = null
    //   }
    // },
    // getNode() {
    //   let a = d3.select('svg').selectAll('g > g')
    //   let nodes = a.nodes()
    //   let links = nodes[0]
    //   let circles = nodes.slice(1)
    //   console.log(links)
    //   console.log(circles)
    //   circles.forEach((circle) => {
    //     console.log(d3.select(circle).id);
    //   })
    // },

    //New graph way
  }
}
</script>
<style scoped>
</style>