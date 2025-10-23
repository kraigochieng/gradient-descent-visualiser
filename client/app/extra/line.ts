	// // Regression line container
	// const lineGroup = svg.append("g").attr("class", "lines");
	// const xLine: [number, number] = [xDomain[0], xDomain[1]];

	// // Create a color scale
	// const colorScale = d3
	// 	.scaleSequential(
	// 		// Fades from a light blue to your red color
	// 		d3.interpolateRgb("#3b82f6", "#ef4444")
	// 	)
	// 	.domain([0, data.epochs.length]);

	// // --- Optional: Sample the data ---
	// // If you have 1000s of epochs, plotting all is heavy.
	// // You can sample them instead. For example, plot
	// // the first 20, then every 50th one.
	// const sampledEpochs = data.epochs.filter((d, i) => {
	// 	// Plot the first 20 epochs, then every 50th epoch after that
	// 	return i < 20 || i % 50 === 0;
	// });
	// // --- End Optional ---

	// // Bind all epoch data to lines
	// lineGroup
	// 	.selectAll("line")
	// 	.data(sampledEpochs) // Use `data.epochs` to plot all lines
	// 	.join("line")
	// 	.attr("x1", x(xLine[0]))
	// 	.attr("x2", x(xLine[1]))
	// 	.attr("y1", (d) => {
	// 		const yVal = d.intercept + d.slope * xLine[0];
	// 		return y(typeof yVal === "number" ? yVal : 0);
	// 	})
	// 	.attr("y2", (d) => {
	// 		const yVal = d.intercept + d.slope * xLine[1];
	// 		return y(typeof yVal === "number" ? yVal : 0);
	// 	})
	// 	.attr("stroke", (d) => colorScale(d.epoch))
	// 	.attr("stroke-width", 1.5)
	// 	.attr("stroke-opacity", 0.2); // Low opacity to see overlap

	// // Add the final, most important line on top, nice and bold
	// const finalYLine = xLine.map(
	// 	(xi) => data.final_intercept + data.final_slope * xi
	// );
	// lineGroup
	// 	.append("line")
	// 	.attr("x1", x(xLine[0]))
	// 	.attr("x2", x(xLine[1]))
	// 	.attr("y1", y(finalYLine[0] ?? 0))
	// 	.attr("y2", y(finalYLine[1] ?? 0))
	// 	.attr("stroke", "#16a34a") // A distinct green color
	// 	.attr("stroke-width", 3);
