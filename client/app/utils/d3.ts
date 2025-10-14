export function getXRange({
	width,
	marginLeft,
	marginRight,
}: {
	width: number;
	marginLeft: number;
	marginRight: number;
}) {
	return [marginLeft, width - marginRight];
}

export function getYRange({
	height,
	marginTop,
	marginBottom,
}: {
	height: number;
	marginTop: number;
	marginBottom: number;
}) {
	return [height - marginBottom, marginTop];
}
