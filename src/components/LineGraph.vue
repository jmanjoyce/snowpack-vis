<!-- eslint-disable @typescript-eslint/no-non-null-assertion -->

<template>
    <svg ref="chart"></svg>
</template>

<script lang="ts">
import { SnowData } from "@/common/interfaces";
import * as d3 from "d3";
import { PropType, defineComponent, ref } from "vue";

export default defineComponent({
    name: "LineGraph",
    emits: ["winter-selected", "winter-hover"],
    data(): {
        info: string;
        svg:
            | d3.Selection<SVGSVGElement, undefined, null, undefined>
            | undefined;
        path:
            | d3.Selection<
                  d3.BaseType | SVGPathElement,
                  (number | undefined)[][] & {
                      z: number | undefined;
                  },
                  SVGGElement,
                  undefined
              >
            | undefined;
        line: d3.Line<[number, number]> | undefined;
        dot: d3.Selection<SVGGElement, undefined, null, undefined> | undefined;
        points: (string | number)[][] | undefined;
        x: d3.ScaleLinear<number, number, never> | undefined;
        y: d3.ScaleLinear<number, number, never> | undefined;
        selectedSet: Set<string>,
    } {
        return {
            x: undefined,
            y: undefined,
            line: undefined,
            info: "",
            svg: undefined,
            path: undefined,
            dot: undefined,
            points: undefined,
            selectedSet: new Set(),
        };
    },
    props: {
        data: {
            type: Object as PropType<SnowData[]>,
            required: true,
        },
        height: Object as PropType<number>,
        width: Object as PropType<number>,
        selected: Object as PropType<string[]>,
    },
    async mounted() {
        console.log("mounted");

        const height = this.height ?? 600;
        const width = this.width ?? 1000;
        const marginTop = 20;
        const marginRight = 20;
        const marginBottom = 30;
        const marginLeft = 30;

        const parentElement = ref("chart");

        this.x = d3
            .scaleLinear()
            .domain([0, d3.max(this.data, (d) => d.dayOfWinter as any)])

            .range([marginLeft, width - marginRight]);

        this.y = d3
            .scaleLinear()
            .domain([0, d3.max(this.data, (d) => d.depthCm as any)])
            .nice()
            .range([height - marginBottom, marginTop]);

        this.svg = d3
            .select(this.$refs.chart as any)
            .attr("width", width)
            .attr("height", height)
            .attr("viewBox", [0, 0, width, height])
            .attr(
                "style",
                "max-width: 100%; height: auto; overflow: visible; font: 10px sans-serif;"
            ) as d3.Selection<SVGSVGElement, undefined, null, undefined>;

        // X-axis
        this.svg
            .append("g")
            .attr("transform", `translate(0,${height - marginBottom})`)
            .call(
                d3.axisBottom(this.x)
                    .ticks(width / 80)
                    .tickFormat((d) => this.dayOfWinterToDate(d as number))
                    .tickSizeOuter(0)
            );

        // Y-axis
        this.svg
            .append("g")
            .attr("transform", `translate(${marginLeft},0)`)
            .call(d3.axisLeft(this.y))
            .call((g) => g.select(".domain").remove())
            .call((g) =>
                g
                    .append("text")
                    .attr("x", -marginLeft)
                    .attr("y", 10)
                    .attr("fill", "currentColor")
                    .attr("text-anchor", "start")
                    .text("Snow Depth (cm)")
            );

        

        this.line = d3.line();

        this.updatePath();
      
        this.dot = this.svg.append("g").attr("display", "none");
        this.dot.append("circle").attr("r", 2.5);
        this.dot.append("text").attr("text-anchor", "middle").attr("y", -8);

        this.path
            ?.filter(({ z }) => {
                return (z as any) === "Average Winter";
            })
            .raise();

        this.svg
            .on("pointerenter", this.pointerEntered)
            .on("pointermove", this.pointerMoved)
            .on("pointerleave", this.pointerLeft)
            .on("touchstart", (event) => event.preventDefault())
            .on("click", this.selectYear);

        // setTimeout(this.animatePath, 1000, "Average Winter");
        this.animatePath("Average Winter");
    },
    watch: {
        selected(oldValue, newValue) {
            if (oldValue != newValue) {
                this.selectedSet.clear(); //
                this.selected?.forEach(item => this.selectedSet.add(item));
                this.stylePath(-1, true);

            }
        },
        data(oldValue, newValue) {
            if (oldValue.length != newValue.length) {
                this.updatePath();
            }
        },
        // data(oldValue: SnowData[], newValue: SnowData[]){
        //     if (oldValue.length != newValue.length ){

        //     }

        // },
    },
    methods: {
        updatePath() {
            this.points = this.data.map((d) => [
                this.x!(d.dayOfWinter),
                this.y!(d.depthCm),
                d.winter,
            ]);

            const groups = d3.rollup(
                this.points,
                (v) => Object.assign(v, { z: v[0][2] }),
                (d) => d[2]
            );

            this.svg?.selectAll("path").remove();

            this.line = d3.line();
            this.path = this.svg!.append("g")
                .attr("fill", "none")
                .attr("stroke-linejoin", "round")
                .attr("stroke-linecap", "round")
                .selectAll("path")
                .data(groups.values())
                .join(
                    (enter) =>
                        enter
                            .append("path")
                            .attr("d", this.line as any)
                            .attr("stroke-width", (d: any) => {
                                if (d.z == "Average Winter") {
                                    return 3;
                                } else {
                                    return 1.5;
                                }
                            })
                            .attr("stroke", (d: any) => {
                                // console.log(d.z);

                                if (d.z == "Average Winter") {
                                    // console.log("yay");
                                    return "red"; // Change color to red for average winter group
                                } else if (this.selectedSet.has(d.z)) {
                                    return "steelblue"; // Keep color as steelblue for other groups // maybe something grayer
                                } else {
                                    return "#ddd";
                                }
                            }),
                    (update) => update,
                    (exit) => {
                        console.log(exit);
                        return exit.attr("stroke", "white");
                    }
                ) as any;
            this.stylePath(-1, false);
        },
        pointerEntered(event: any) {
            this.stylePath(-1, false);

            this.dot?.attr("display", null);
        },
        // drawLines(){

        // },
        pointerMoved(event: any) {
            if (this.data.length ==0) return;
            const [xm, ym] = d3.pointer(event);
            const i = d3.leastIndex(this.points!, ([x, y]) =>
                Math.hypot((x as number) - xm, (y as number) - ym)
            );
            const [x, y, k] = this.points![i!];
            this.stylePath(i ?? -1, false);
            if (i) {
                this.$emit("winter-hover", i);
            }

            this.dot?.attr("transform", `translate(${x},${y})`);
            this.dot?.select("text").text(k as any);
            (this.svg?.property("value", this.data![i!]) as any).dispatch(
                "input",
                {
                    bubbles: true,
                }
            );
        },
        pointerLeft(event: any) {
            this.stylePath(-1, false);
            this.dot?.attr("display", "none");
            (this.svg as any).node().value = null;
            (this.svg as any).dispatch("input", { bubbles: true });
            this.$emit("winter-hover", undefined);
        },
        selectYear(event: any) {
            const [xm, ym] = d3.pointer(event);
            const i = d3.leastIndex(this.points!, ([x, y]) =>
                Math.hypot((x as number) - xm, (y as number) - ym)
            );
            const [x, y, k] = this.points![i!];
            this.$emit("winter-selected", k);
        },
        highlightYear() {
            this.stylePath(-1, true);
        },
        stylePath(hoverId: number, justSelected: boolean) {
            const [x, y, k] =
                hoverId == -1 ? [-1, -1, -1] : this.points![hoverId!];

            // If just selected add a animation for the line to become
            // uncovered
            // Todo add color palate.
            this.path
                ?.style("stroke", ({ z }) => {
                    if ((z as any) == "Average Winter") {
                        return "#F44336";
                    } else if (this.selectedSet.has(z as any)) {
                        return "#0091EA";
                    } else if (z === k) {
                        return "#bbb";
                    } else {
                        return "#ddd";
                    }
                })
                .style("stroke-width", ({ z }) => {
                    if (this.selectedSet.has(z as any)) {
                        return 2.5;
                    } else if ((z as any) == "Average Winter") {
                        return 3;
                    } else if (z === k) {
                        return 2.5;
                    } else {
                        return 1.5;
                    }
                })
                .filter(
                    ({ z }) =>
                        this.selectedSet.has(z as any) ||
                        (z as any) == "Average Winter" ||
                        z == k
                )
                .raise();
            if (justSelected) { // Gotta get most recently changed
                this.animatePath(this.selected![0]);
            }
        },
        animatePath(winter: string) {
            const selectedPath = this.path?.filter(({ z }) => {
                return (z as any) === winter;
            });

            // Now you can get the total length of the selected path
            const node = selectedPath?.node();
            if (node) {
                const length = (node as any).getTotalLength();
                selectedPath
                    ?.attr("stroke-dasharray", length + " " + length)
                    .attr("stroke-dashoffset", length)
                    .transition()
                    .ease(d3.easeLinear)
                    .attr("stroke-dashoffset", 0)
                    .duration(1000);
            }
        },
        dayOfWinterToDate(dayOfWinter: number): string {
            // Start date is November 1st of the current winter season
            const baseDate = new Date(2023, 10, 1); // Month is 0-based, so 10 = November
            const targetDate = new Date(baseDate);
            targetDate.setDate(baseDate.getDate() + dayOfWinter - 1);
            
            // Format as MMM DD (e.g., "Nov 01", "Dec 15", etc.)
            return targetDate.toLocaleDateString('en-US', { month: 'short', day: '2-digit' });
        },
    },
});
</script>
