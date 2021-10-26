<!--Whole component is for testing-->
<template>
  <div>
    <svg width="560" height="360"></svg>
  </div>
  <button @click="createExampleGraph"></button>
</template>

<script>
import * as d3 from 'd3'

export default {
  name: "Example",
  methods: {
    createExampleGraph() {

      let links = [
        {source: "Oracle", target: "Google", type: "suit"},
        {source: "Oracle", target: "Google", type: "licensing"},
        {source: "Google", target: "Oracle", type: "resolved"}
      ]

      links.sort(function(a,b) {
        if (a.source > b.source) {return 1;}
        else if (a.source < b.source) {console.log(links);return -1;}
        else {
            if (a.target > b.target) {return 1;}
            if (a.target < b.target) {return -1;}
            else {return 0;}
        }
      });

      for (let i=0; i<links.length; i++) {
        if (i != 0 &&
          links[i].source == links[i-1].source &&
          links[i].target == links[i-1].target) {
              links[i].linkPrio = links[i-1].linkPrio + 1;
          }
        else {links[i].linkPrio = 1;};
      }

      let types = [
        "licensing",
        "suit",
        "resolved"
      ]

      let nodes = [
        {id: "Oracle"},
        {id: "Google"}
      ]

      let svg = d3.select("svg"),
          width = +svg.attr("width"),
          height = +svg.attr("height"),
          color = d3.scaleOrdinal(types, d3.schemeCategory10)

      svg = svg.append("g").attr("transform", "translate(" + width / 2 + "," + height / 2 + ")")

      let simulation = d3.forceSimulation(nodes)
          .force("link", d3.forceLink(links).id(d => d.id))
          .force("charge", d3.forceManyBody().strength(-1000))
          .force("x", d3.forceX())
          .force("y", d3.forceY());

      // Per-type markers, as they don't inherit styles.
      svg.append("defs").selectAll("marker")
          .data(types)
          .join("marker")
          .attr("id", d => `arrow-${d}`)
          .attr("viewBox", "0 -5 10 10")
          .attr("refX", 15)
          .attr("refY", -0.5)
          .attr("markerWidth", 6)
          .attr("markerHeight", 6)
          .attr("orient", "auto")
          .append("path")
          .attr("fill", color)
          .attr("d", "M0,-5L10,0L0,5");

      let link = svg.append("g")
          .attr("fill", "none")
          .attr("stroke-width", 1.5)
          .selectAll("path")
          .data(links)
          .join("path")
          .attr("stroke", d => color(d.type))
          .attr("marker-end", d => `url(${new URL(`#arrow-${d.type}`, location)})`);

      let node = svg.append("g")
          .attr("fill", "currentColor")
          .attr("stroke-linecap", "round")
          .attr("stroke-linejoin", "round")
          .selectAll("g")
          .data(nodes)
          .join("g")

      node.append("circle")
          .attr("stroke", "white")
          .attr("stroke-width", 1.5)
          .attr("r", 4);

      node.append("text")
          .attr("x", 8)
          .attr("y", "0.31em")
          .text(d => d.id)
          .clone(true).lower()
          .attr("fill", "none")
          .attr("stroke", "white")
          .attr("stroke-width", 3);

      simulation.on("tick", () => {
        link.transition().attr("d", this.linkArc).duration(100).attr("opacity", 10);
        node.attr("transform", d => `translate(${d.x},${d.y})`);
      });
    },
    linkArc(d) {
      // let r = Math.hypot(d.target.x - d.source.x, d.target.y - d.source.y, 75/d.linkPrio);
      let dx = d.target.x - d.source.x,
          dy = d.target.y - d.source.y,
          dr = 75/d.linkPrio;
      return "M" + d.source.x + "," + d.source.y + "A" + dr + "," + dr + " 0 0,1 " + d.target.x + "," + d.target.y;
    },
  }
}
</script>

<style scoped>
.line {
    stroke: blue;
    stroke-width: 1.5px;
    fill: white;
}
circle {
    fill: red;
}
#marker {
  stroke: black;
    fill: black;
}
</style>