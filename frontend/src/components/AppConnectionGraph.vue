<template>
  <div class="graph-view col-md-6">
    <svg width="560" height="360"></svg>
  </div>
</template>
<script>
import * as d3 from 'd3'

export default {
  props: ['activeUsersList', 'activeUsersLink', 'messageSent', 'messageFrom', 'messageTo'],
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
      let onlineLinks = this.activeUsersLink
      let nodes = [],
          links = [];

      // Iterate through users from parent component
      this.activeUsersList.forEach((node) => {
        nodes.push({
          id: node.id
        })
      })

      // Iterate through created chat sessions between users from parent component
      if (nodes.length !== 0) {
        for (let n = 0; n < onlineLinks.length; n++) {
          let linkObject = {source: null, target:null, linkPrio:1}
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
      }

      if (this.messageSent[0] == true) {
        links.forEach((link) => {
          if (link.source.id == this.messageFrom[0] && link.target.id == this.messageTo) {
            let additionalPath = {
              ...link,
              linkPrio: 2,
            }
            links.push(additionalPath)
          }
        })
      }

      // Create new graph simulation based on nodes and links data
      let simulation = d3.forceSimulation(nodes)
          .force("charge", d3.forceManyBody().strength(-1000))
          .force("link", d3.forceLink(links).id(d => d.id).distance(100))
          .force("x", d3.forceX())
          .force("y", d3.forceY())
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
          .attr("fill", "none")
          .selectAll(".link")

      // Create new node tag for graph template
      let node = g.append("g")
          .attr("stroke", "#000")
          .selectAll(".node");

      // Recreate graph simulation with new data
      restart();

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
        link = link.enter().append("g");
        link = link.append("path");
        link.attr('class', getPathPrio);
        if (!d3.selectAll("path.secondary").empty()) {
          let secondary_link = d3.select("path.secondary")
          secondary_link.attr('id', 'sent-message')
          let g = secondary_link.select(function() { return this.parentNode; })
          g.append("text")
            .style("font-size",15)
            .style("fill","#000")
            .attr("dy",-5)
            .append("textPath")
            .attr("xlink:href","#sent-message")
            .style("text-anchor","middle")
            .attr("startOffset","50%")
            .text("Sending message...")
            .attr('stroke-width', 0)
            .style("stroke-dasharray", 'none');
        }

        // Update and restart the simulation.
        simulation.nodes(nodes);
        simulation.force("link").links(links);
        simulation.alpha(1).restart();
      }

      // Building appearance and animations of the graph
      function ticked() {
        node.attr('transform', function (d) {return 'translate(' + d.x + ',' + d.y + ')' })
        link.attr("d", linkArc);
      }

      function linkArc(d) {
        let dx = d.target.x - d.source.x,
            dy = d.target.y - d.source.y,
            dr = 95/d.linkPrio;  //linkPrio is defined above
        return "M" + d.source.x + "," + d.source.y + "A" + dr + "," + dr + " 0 0,1 " + d.target.x + "," + d.target.y;
      }

      function getPathPrio(path_priority) {
        if (path_priority.linkPrio > 1) {
          return 'secondary'
        } else {
          return 'primary'
        }
      }
    },
  }
}
</script>
<style scoped>
.graph-view {
  background-image: url(https://www.amcharts.com/wp-content/uploads/2013/12/demo_910_none-1.png);
  background-size: 110%;
  background-position: center;
}
::v-deep .secondary {
  stroke-dasharray: none;
  stroke: #000;
  stroke-width: 4;
}

::v-deep .secondary {
    animation-name: periodicfading;
    animation-duration: 1s;
    animation-iteration-count: infinite;
    animation-timing-function: linear;
    animation-delay: 0s;
}

@keyframes periodicfading {
    0% {
        opacity: 0.3;
    }
    50% {
        opacity: 1.0;
    }
    100% {
        opacity: 0.3;
    }
}
</style>