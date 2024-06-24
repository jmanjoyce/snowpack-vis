<template>
    <v-app>
        <v-app-bar color="#03A9F4" dark>
            <!-- Title -->
            <v-toolbar-title>{{ msg }}</v-toolbar-title>
        </v-app-bar>
        <div class="home">
            <!-- <div class="title">
            <h1>{{ msg }}</h1>
            </div> -->

            <div class="spacer"></div>
            <div class="main-display">
                <div class="left-side-bar">
                    <v-row justify="center">
                        <v-col aling="center" justify="center" cols="10">
                            <v-autocomplete
                                chips
                                multiple
                                variant="solo"
                                v-if="winters"
                                label="Select Winter"
                                :items="winters"
                                v-model="selected"
                            >
                            </v-autocomplete>
                            <v-card
                                variant="elevated"
                                v-if="hoverPoint"
                                :class="['mx-auto', 'display-card']"
                                max-width="400"
                                mb="4"
                            >
                                <v-card-text class="pb-2">
                                    <v-row align="center" no-gutters>
                                        <v-col class="text-h3" cols="12">
                                            {{
                                                Math.floor(hoverPoint?.depthCm)
                                            }}
                                            cm
                                        </v-col>
                                    </v-row>
                                    <v-row align="center" no-gutters>
                                        <v-col
                                            :class="['text-h5', getPercentOfAvg()! < 100 ? 'red-text': 'green-text']"
                                        >
                                            {{ getPercentOfAvg() }}%
                                        </v-col>
                                    </v-row>
                                </v-card-text>
                                <v-divider></v-divider>

                                <v-card-actions class="d-flex justify-center">
                                    <v-list-item>
                                        <v-list-item-content>
                                            <v-list-item-subtitle>
                                                {{ getHoverPointDate() }}
                                            </v-list-item-subtitle>
                                        </v-list-item-content>
                                    </v-list-item>
                                </v-card-actions>
                            </v-card>

                            <v-card
                                variant="elevated"
                                class="mx-auto display-card"
                                max-width="400"
                                mb="4"
                            >
                                <v-list  v-for="winter in selected"
                                :key="winter">
                                <v-list-item>
                                    <v-list-item-title>{{ winter }}</v-list-item-title>
                                    <v-list-item-content>
                                <!-- <v-card-text class="pb-2"> -->
                                    <v-row align="center" no-gutters>
                                        <v-col class="text-h3" cols="12">
                                            
                                        </v-col>
                                    </v-row>

                                    <v-list-item-content :class="[
                                                'text-h5',
                                                getWinterPecentOfAvg(winter) <
                                                100
                                                    ? 'red-text'
                                                    : 'green-text',
                                            ]"
                                            :color="
                                                getWinterPecentOfAvg(winter) <
                                                100
                                                    ? 'red'
                                                    : 'green'
                                            ">
                                            {{ getWinterPecentOfAvg(winter) }}%
                                            of Avg

                                    </v-list-item-content>

                                    <!-- <v-row align="center" no-gutters>
                                        <v-col
                                            :class="[
                                                'text-h5',
                                                getWinterPecentOfAvg(winter) <
                                                100
                                                    ? 'red-text'
                                                    : 'green-text',
                                            ]"
                                            :color="
                                                getWinterPecentOfAvg(winter) <
                                                100
                                                    ? 'red'
                                                    : 'green'
                                            "
                                        >
                                            
                                        </v-col>
                                    </v-row> -->
                                <!-- </v-card-text> -->
                                <!-- <v-divider></v-divider> -->
                                <!-- <v-card-actions class="d-flex justify-center"> -->
                                    <!-- <v-list-item>
                                        <v-list-item-content>
                                            <v-list-item-subtitle>
                                                Max depth
                                                {{ getMaxDepth(winter) }}cm
                                            </v-list-item-subtitle>
                                        </v-list-item-content>
                                    </v-list-item> -->
                                </v-list-item-content>
                            </v-list-item>
                                <!-- </v-card-actions> -->
                            </v-list>
                            </v-card>
                        </v-col>
                    </v-row>
                </div>
                <div class="vis-tool" ref="visTool">
                    <v-card variant="elevated">
                        <v-card-title>Hermit Lake Snow Depth</v-card-title>
                        <v-card-text>
                            <LineGraph
                                v-if="snowData"
                                @winter-selected="selectWinter"
                                @winter-hover="hoverWinter"
                                :selected="selected"
                                :data="snowDataDisplayed ?? []"
                            ></LineGraph>
                        </v-card-text>
                    </v-card>
                </div>
                <div class="right-side-bar">
                    <v-row justify="center">
                        <v-col aling="center" justify="center" cols="10">
                            <v-card>
                                <v-card-title>Options</v-card-title>
                                <v-card-text>
                                    <v-form>
                                        <v-checkbox
                                            color="#03A9F4"
                                            label="Show Average"
                                            v-model="showAvg"
                                        ></v-checkbox>
                                        <v-checkbox
                                            label="All years"
                                            v-model="showUnselected"
                                        ></v-checkbox>
                                    </v-form>
                                </v-card-text>
                            </v-card>
                            <div class="spacer"></div>
                            <v-card>
                                <v-card-title> Stations </v-card-title>
                                <v-card-text>
                                    <v-form>
                                        <v-checkbox
                                            color="#03A9F4"
                                            label="Hermit Lake"
                                        ></v-checkbox>
                                        <v-checkbox
                                            label="Harvard Cabin"
                                        ></v-checkbox>
                                        <v-checkbox
                                            label="Gray Knob"
                                        ></v-checkbox>
                                    </v-form>
                                </v-card-text>
                            </v-card>
                        </v-col>
                    </v-row>
                </div>
            </div>
        </div>
    </v-app>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import LineGraph from "./LineGraph.vue";
import { SnowData } from "@/common/interfaces";
import * as d3 from "d3";

export default defineComponent({
    name: "MwacVis",
    props: {
        msg: String,
    },
    components: {
        LineGraph,
    },
    data(): {
        avgWinterMap: Map<number, number> | undefined;
        snowData: SnowData[] | undefined;
        snowDataDisplayed: SnowData[] | undefined;
        hoverPoint: SnowData | undefined;
        winters: string[] | undefined;
        selected: string[] | undefined;
        maxVisWid: number;
        maxVisLen: number;
        showAvg: boolean;
        showUnselected: boolean;
    } {
        return {
            maxVisWid: 0,
            maxVisLen: 0,
            snowDataDisplayed: undefined,
            avgWinterMap: undefined,
            hoverPoint: undefined,
            winters: undefined,
            selected: undefined,
            snowData: undefined,
            showAvg: true,
            showUnselected: true,
        };
    },
    mounted() {
        this.updateDimensions();
        this.genData();
    },
    watch: {
        showAvg(oldValue, newValue) {
            if (oldValue != newValue) {
                console.log("avg");
                this.toggleAvg();
            }
        },
        showUnselected(oldValue, newValue) {
            if (oldValue != newValue) {
                this.toggleDisplayAll();
            }
        },
        selected(){
            // Needs to update data display when data is not being displayed.
        }
    },
    methods: {
        updateDimensions() {
            // For updating dimensions of svg
            const visTool = this.$refs.visTool;
            if (visTool) {
                const rect = (visTool as any).getBoundingClientRect();
                this.maxVisWid = rect.width;
                this.maxVisLen = rect.height;
            }
        },
        getHoverPointDate() {
            if (this.hoverPoint?.winter === "Average Winter") {
                return this.getMonthDayFromDOW(this.hoverPoint.dayOfWinter);
            } else {
                return this.hoverPoint?.date?.toDateString();
            }
        },
        getMaxDepth(winter: string) {
            var max = 0;
            this.snowData
                ?.filter((d) => d.winter === winter)
                .forEach((depth) => {
                    max = Math.max(depth.depthCm, max);
                });
            return Math.floor(max);
        },
        hoverWinter(hover: undefined | number) {
            if (hover && this.snowData) {
                this.hoverPoint = this.snowData[hover];
            } else {
                this.hoverPoint = undefined;
            }
        },
        getMonthDayFromDOW(dayOfWinter: number) {
            const referenceDate = new Date(2001, 10, 1); // Month is 0-based in JavaScript

            // Add the number of days to the reference date
            const targetDate = new Date();
            targetDate.setDate(referenceDate.getDate() + dayOfWinter - 1);

            const monthNames = [
                "January",
                "February",
                "March",
                "April",
                "May",
                "June",
                "July",
                "August",
                "September",
                "October",
                "November",
                "December",
            ];
            const month = monthNames[targetDate.getMonth()];
            return `${month}, ${targetDate.getDate()} `;
        },
        getWinterPecentOfAvg(winter: string): number {
            // Get information about selected winter.
            const currentSelectedWinter: SnowData[] =
                this.snowData?.filter((dtp) => dtp.winter == winter) ??
                [];
            const daySet: Set<number> = new Set(
                currentSelectedWinter.map((w) => w.dayOfWinter)
            );
            const matchingAvgDays = this.snowData?.filter((d) => {
                return (
                    d.winter === "Average Winter" && daySet.has(d.dayOfWinter)
                );
            });
            const avgSum =
                matchingAvgDays?.reduce((acc, val) => acc + val.depthCm, 0) ??
                NaN;
            const selectedSum =
                currentSelectedWinter?.reduce(
                    (acc, val) => acc + val.depthCm,
                    0
                ) ?? NaN;
            if (isNaN(avgSum) || isNaN(selectedSum)) {
                return NaN;
            }
            return Math.floor((selectedSum / avgSum) * 100);
        },
        getPercentOfAvg() {
            if (this.hoverPoint && this.avgWinterMap) {
                var avgDepth =
                    this.avgWinterMap.get(this.hoverPoint.dayOfWinter) ?? 1;
                console.log(avgDepth);
                return Math.floor((this.hoverPoint.depthCm / avgDepth) * 100);
            }
        },
        initWinters(winters: string[]) {
            this.winters = winters;
        },
        toggleAvg() {
            console.log("avg in toggle", this.showAvg);
            if (this.showAvg) {
                const avgYear: SnowData[] | undefined = this.snowData?.filter(
                    (data) => data.winter == "Average Winter"
                );
                this.snowDataDisplayed = this.snowDataDisplayed?.concat(
                    avgYear ?? []
                );
            } else {
                this.snowDataDisplayed = this.snowDataDisplayed?.filter(
                    (data) => data.winter != "Average Winter"
                );
            }
        },
        toggleDisplayAll() {
            const selectedSet: Set<string> = new Set(this.selected);
            if (this.showUnselected) {
                if (this.showAvg) {
                    this.snowDataDisplayed = this.snowData;
                } else {
                    const unselected = this.snowData?.filter(
                        (data) =>
                            !selectedSet.has(data.winter) &&
                            data.winter != "Average Winter"
                    );
                    this.snowDataDisplayed = this.snowDataDisplayed?.concat(
                        unselected ?? []
                    );
                }
            } else {
                this.snowDataDisplayed = this.snowDataDisplayed?.filter(
                    (data) =>
                        selectedSet.has(data.winter) ||
                        data.winter == "Average Winter"
                );
            }
        },
        selectWinter(winter: string) {
            const selectedSet: Set<string> = new Set(this.selected);
            if (selectedSet.has(winter)) {
                selectedSet.delete(winter);
                this.selected = [...selectedSet];
                
            } else {
                this.selected = this.selected?.concat(winter) ?? [];
            }
        },
        async genData() {
            const historicalDataRaw = await d3.csv(
                "cleaned_hermit_lake_snowdepth.csv"
            );

            const winters: Set<string> = new Set();

            const historicalData: SnowData[] = historicalDataRaw.map((row) => {
                winters.add(row.winter);
                return {
                    date: new Date(row.date),
                    depthCm: +row.depth_cm,
                    year: +row.year,
                    month: +row.month,
                    day: +row.day,
                    monthDay: row.month_day,
                    winter: row.winter,
                    dayOfWinter: +row.day_of_winter,
                };
            });

            this.winters = [...winters];

            const historicalAvgRaw = await d3.csv("historical_averages.csv");

            const avgWinterMap: Map<number, number> = new Map();

            const avgData: SnowData[] = historicalAvgRaw.map((row) => {
                avgWinterMap.set(+row.day_of_winter, +row.depth_cm);
                return {
                    depthCm: +row.depth_cm,
                    winter: "Average Winter",
                    dayOfWinter: +row.day_of_winter,
                };
            });
            this.avgWinterMap = avgWinterMap;

            const snow = [...historicalData, ...avgData];
            this.snowData = snow;
            this.snowDataDisplayed = this.snowData;

            this.hoverPoint = snow[30];
            console.log(this.snowData);
        },
    },
});
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
@import "../styles/colors";

.green-text {
    color: $success-color;
}

.spacer {
    margin-top: 3dvh;
}

.red-text {
    color: $error-color;
}

.display-card {
    margin: 10px;
}

// .v-input--checkbox:not(:first-child) {
//   margin-top: -40px; /* Adjust negative margin to reduce spacing */
// }

.home {
    display: flex;
    flex-direction: column;
    flex-wrap: nowrap;
    width: 100vw;
    margin-top: 8vh;
}
.title {
    background-color: $primary-color;
    color: $text-color;
    display: flex;
    justify-content: center;
}

.main-display {
    display: flex;
    flex-direction: row;
    justify-content: center;
    flex: 1;
}

.left-side-bar {
    display: flex;
    flex: 18%;
    flex-direction: column;
    flex-wrap: nowrap;
}

.right-side-bar {
    display: flex;
    flex: 15%;
    flex-direction: column;
    flex-wrap: nowrap;
}

.vis-tool {
    display: flex;
    flex: 67%;
    box-sizing: border-box;
}

h3 {
    margin: 40px 0 0;
}
ul {
    list-style-type: none;
    padding: 0;
}
li {
    display: inline-block;
    margin: 0 10px;
}
a {
    color: #42b983;
}
</style>
