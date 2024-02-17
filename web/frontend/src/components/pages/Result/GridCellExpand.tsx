import { memo, useEffect, useRef, useState } from "react";
import { Box, Popper, Paper, Typography } from "@mui/material";
import { isOverflown } from "@mui/x-data-grid/utils/domUtils";
import { GridRenderCellParams } from "@mui/x-data-grid";

interface Props {
  value: string;
  width: number;
}

const GridCellExpand = memo((props: Props) => {
  const { width, value } = props;
  const wrapper = useRef<HTMLDivElement | null>(null);
  const cellDiv = useRef(null);
  const cellValue = useRef(null);
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const [showFullCell, setShowFullCell] = useState(false);
  const [showPopper, setShowPopper] = useState(false);

  const handleMouseEnter = () => {
    const isCurrentlyOverflown = isOverflown(cellValue.current!);
    setShowPopper(isCurrentlyOverflown);
    setAnchorEl(cellDiv.current);
    setShowFullCell(true);
  };

  const handleMouseLeave = () => {
    setShowFullCell(false);
  };

  useEffect(() => {
    if (!showFullCell) {
      return undefined;
    }

    const handleKeyDown = (nativeEvent: KeyboardEvent) => {
      if (nativeEvent.key === "Escape" || nativeEvent.key === "Esc") {
        setShowFullCell(false);
      }
    }

    document.addEventListener("keydown", handleKeyDown);

    return () => {
      document.removeEventListener("keydown", handleKeyDown);
    };
  }, [setShowFullCell, showFullCell]);

  return (
    <Box
      ref={wrapper}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      sx={{
        alignItems: "center",
        lineHeight: "24px",
        width: "100%",
        height: "100%",
        position: "relative",
        display: "flex",
      }}
    >
      <Box
        ref={cellDiv}
        sx={{
          height: "100%",
          width,
          display: "block",
          position: "absolute",
          top: 0,
        }}
      />
      <Box
        ref={cellValue}
        sx={{
          whiteSpace: "nowrap",
          overflow: "hidden",
          textOverflow: "ellipsis",
        }}
      >
        {value}
      </Box>
      {showPopper && (
        <Popper
          open={showFullCell && anchorEl !== null}
          anchorEl={anchorEl}
          sx={{ width }}
        >
          <Paper
            elevation={1}
            sx={(theme) => ({
              minHeight: wrapper.current?.offsetHeight,
              bgcolor: theme.palette.background.default,
            })}
          >
            <Typography variant="body2" sx={{ padding: 1 }}>
              {/* value with any kind of dashed replaced by non-breakable dash to prevent splitting value between lines */}
              {value.replace(/-/g, "‑")}
            </Typography>
          </Paper>
        </Popper>
      )}
    </Box>
  );
});

export const renderCellExpand = (params: GridRenderCellParams) => {
  return (
    <GridCellExpand value={params.value || ''} width={params.colDef.computedWidth} />
  );
}

export default GridCellExpand;