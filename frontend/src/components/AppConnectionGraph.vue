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
  props: ['activeUsersList', 'activeUsersLink'],
  data () {
    return {}
  },
  methods: {
    createGraph() {
      // Get svg tag from template
      let svg = d3.select("svg"),
          width = +svg.attr("width"),
          height = +svg.attr("height"),
          // Create color range for new elements
          color = d3.scaleOrdinal()
            .domain(d3.range(this.activeUsersList.length))
            .range(d3.schemeCategory10)

      // Create nodes (for circles) and links (for links between circles) arrays
      let onlineNodes = this.activeUsersList
      let onlineLinks = this.activeUsersLink
      let nodes = [],
          links = [];

      // Iterate through users from parent component
      onlineNodes.forEach((node) => {
        nodes.push(node)
      })

      // Iterate through created chat sessions between users from parent component
      for (let n = 0; n < onlineLinks.length; n++) {
        let linkObject = {source: null, target:null}
        for (let i = 0; i < nodes.length; i++) {
          if (nodes[i].id == onlineLinks[n].source) {
            linkObject.source = nodes[i]
          }
          if (nodes[i].id == onlineLinks[n].target) {
            linkObject.target = nodes[i]
          }
        }
        links.push(linkObject)
      }

      // Create new graph simulation based on nodes and links data
      let simulation = d3.forceSimulation(nodes)
          .force("charge", d3.forceManyBody().strength(-400))
          .force("link", d3.forceLink(links).distance(200))
          .force("x", d3.forceX())
          .force("y", d3.forceY())
          .alphaTarget(1)
          .on("tick", ticked)

      // Remove previous published graph template
      svg.select("g").remove()

      // Create new graph template
      let g = svg.append("g").attr("transform", "translate(" + width / 2 + "," + height / 2 + ")")

      // Create new link tag for graph template
      let link = g.append("g")
          .style("stroke-dasharray", ("3, 3"))
          .attr("stroke", "#000")
          .attr("stroke-width", 6)
          .selectAll(".link")

      // Create new node tag for graph template
      let node = g.append("g")
          .attr("stroke", "#000")
          .selectAll(".node");

      // for (let n = 0; n < links.length; n++) {
      //   console.log('888888888888888888888')
      //   console.log(links[n])
      // }
      //
      // for (let n = 0; n < links.length; n++) {
      //   console.log('SOURCE = ' + links[n])
      //   console.log('TARGET = ' + links[n])
      //   for (let i = 0; i < nodes.length; i++) {
      //     if (nodes[i].id == links[n].source) {
      //       console.log('SOURCE LINK = ' + links[n])
      //       console.log('SOURCE NODE PROXY = ' + nodes[i])
      //     }
      //   }
      // }

      // for (let link_piece in this.activeUserLinks) {
      //   console.log(link_piece)
      //   for (let node in nodes) {
      //     console.log(node)
      //     if (link.source == node.id) {
      //       console.log('opop')
      //     }
      //   }
      // }
      // for (let i = 0; i < nodes.length; i++) {
      //   let start = i
      //   let end = ++i
      //   links.push({
      //     source: nodes[start],
      //     target: nodes[end]
      //   });
      // }

      // Recreate graph simulation with new data
      restart();

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

      // Simulation restart for data from parent components
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

      // Building appearance and animations of the graph
      function ticked() {
        node.attr('transform', function (d) { return 'translate(' + d.x + ',' + d.y + ')' })

        link.attr("x1", function(d) { return d.source.x; })
            .attr("y1", function(d) { return d.source.y; })
            .attr("x2", function(d) { return d.target.x; })
            .attr("y2", function(d) { return d.target.y; });
      }
    },
  }
}
</script>
<style scoped>
</style>