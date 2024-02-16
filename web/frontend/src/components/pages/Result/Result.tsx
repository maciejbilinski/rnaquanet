import { useEffect, useState } from "react";
import {
  Box,
  Card,
  CircularProgress,
  Step,
  StepLabel,
  Stepper,
  Typography,
  useMediaQuery,
  useTheme,
} from "@mui/material";
import { DataGrid, GridColDef } from "@mui/x-data-grid";
import {
  MaterialReactTable,
  useMaterialReactTable,
  type MRT_ColumnDef,
} from "material-react-table";

import { API_ADDRESS, REQUEST_RETRY_DELAY } from "../../../../config";
import { styles } from "../../../utils/styles";
import { steps, getCurrentStep } from "./steps";

const Result = () => {
  const theme = useTheme();
  const isSmallScreen = useMediaQuery(theme.breakpoints.down("md"));
  const [response, setResponse] = useState<TaskResult>();
  const [step, setStep] = useState<Step>({
    id: 0,
    status: "loading",
  });

  const columnHeaders: MRT_ColumnDef<FileResult>[] = [
  {
    accessorKey: "name",
    header: "File name",
  },
  {
    header: "Model",
    accessorFn: (row) => Number(row.selectedModel) + 1,
  },
  { accessorKey: "selectedChain", header: "Chain" },
  {
    accessorKey: "rmsd",
    header: response?.analysis_type === "local" ? "Average RMSD" : "RMSD",
    accessorFn: (row) =>
      row.status === "SUCCESS" && row.rmsd
        ? row.rmsd.toFixed(4)
        : "Invalid file!",
    muiTableHeadCellProps: {
      align: "right",
    },
    muiTableBodyCellProps: {
      align: "right",
    },
    muiTableFooterCellProps: {
      align: "right",
    },
  },
];

const columnHeadersDesc: GridColDef<Descriptor>[] = [
  {
    field: "name",
    headerName: "Descriptor name",
    flex: 1,
  },
  {
    field: "residue_range",
    headerName: "Residue range",
    flex: 1,
  },
  {
    field: "sequence",
    headerName: "Sequence",
    flex: 1,
  },
  {
    field: "rmsd",
    headerName: "RMSD",
    valueFormatter: (row) => row.value.toFixed(4),
    type: "number",
    flex: 1,
  },
];

  const fetchData = async () => {
    try {
      const task_id = location.pathname.split("/").pop();
      const res = await fetch(`${API_ADDRESS}/check_rmsd/${task_id}`, {
        method: "GET",
      });

      // parse received data
      const json: TaskResult = {
        status_code: res.status,
        ...(res.status === 200 ? await res.json() : {}),
      };
      setResponse(json);

      // if file has not yet finished processing and there were no errors
      // set a simeout to check again in `REQUEST_RETRY_DELAY` ms
      if (
        json.status_code === 200 &&
        json.status !== "DONE" &&
        json.status !== "ERROR"
      ) {
        setTimeout(fetchData, REQUEST_RETRY_DELAY);
      }
    } catch (error) {
      setResponse({ status_code: 500 });
      setTimeout(fetchData, REQUEST_RETRY_DELAY);
    }
  };

  useEffect(() => {
    setTimeout(fetchData, 1000);
  }, []);

  useEffect(() => {
    setStep(getCurrentStep(step.id, response));
  }, [response]);

  const table = useMaterialReactTable({
    // @ts-ignore
    columns: columnHeaders,
    data: response?.files ?? [],
    initialState: { pagination: { pageSize: 10, pageIndex: 0 } },
    muiPaginationProps: {
      showRowsPerPage: false,
    },

    mrtTheme: (theme) => ({
      baseBackgroundColor:
        theme.palette.mode === "light" ? "#ffffff" : "#1e1e1e",
    }),

    //custom expand button rotation
    muiExpandButtonProps: ({ row }) => ({
      sx: {
        transform: row.getIsExpanded() ? "rotate(180deg)" : "rotate(-90deg)",
        transition: "transform 0.2s",
      },
    }),

    //conditionally render detail panel
    ...(response?.analysis_type === "local"
      ? {
          renderDetailPanel: ({ row }) => (
            <DataGrid
              columns={columnHeadersDesc}
              rows={row.original.descriptors ?? []}
              hideFooter
            />
          ),
        }
      : {}),
  });

  return (
    <Card
      sx={{
        ...styles.mainCard,
        minHeight: 640,
      }}
    >
      <Stepper
        activeStep={step.id}
        orientation={isSmallScreen ? "vertical" : "horizontal"}
      >
        {steps.map((s, i) => {
          const cur = step.id === i;
          const failed = cur && step.status === "failed";
          const loading = cur && step.status === "loading";
          const stepCompleted = step.id > i;

          return (
            <Step key={i}>
              <StepLabel
                error={failed}
                icon={loading && <CircularProgress size="1.5rem" />}
                optional={
                  cur && (
                    <Typography fontSize="12px">
                      {step.specialDescription ??
                        "Page will refresh automatically"}
                    </Typography>
                  )
                }
              >
                {stepCompleted ? s.labelFinished : s.label}
              </StepLabel>
            </Step>
          );
        })}
      </Stepper>

      {response?.status === "DONE" && response.files && (
        <Box
          sx={{
            mt: 5,
            display: "flex",
            justifyContent: "center",
          }}
        >
          <MaterialReactTable table={table} />
        </Box>
      )}
    </Card>
  );
};

export default Result;
