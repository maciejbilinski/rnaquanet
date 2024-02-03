import { SxProps } from "@mui/material";

export const styles: { [name: string]: SxProps } = {
  mainCard: {
    display: "flex",
    flexDirection: "column",
    mx: { xs: 0, md: 1 },
    px: { xs: 2, md: 6 },
    py: 4,
    gap: 4,
  },

  slimScrollbar: {
    /* width */
    "::-webkit-scrollbar": {
      width: 6,
    },
    /* Track */
    "::-webkit-scrollbar-track": {
      background: "#f1f1f1",
    },
    /* Handle */
    "::-webkit-scrollbar-thumb": {
      background: "#888",
    },
    /* Handle on hover */
    "::-webkit-scrollbar-thumb:hover": {
      background: "#555",
    },
  } as SxProps,
};
