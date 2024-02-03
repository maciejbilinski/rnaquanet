import { useState } from "react";
import { Accordion, AccordionDetails, AccordionSummary, Box, Card, IconButton, Typography } from "@mui/material";
import VisibilityIcon from '@mui/icons-material/Visibility';
import VisibilityOffIcon from '@mui/icons-material/VisibilityOff';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import Fade from '@mui/material/Fade';

import { styles } from "../../../utils/styles";
import { projectName } from "../../../../config";

const ProjectInfo = () => {
  const [expanded, setExpanded] = useState<boolean>(false);

  return (
    <Card
      sx={{
        ...styles.mainCard,
        py: 6,
      }}
    >
      <Box sx={{
        display: "flex",
        flexDirection: "column",
        gap: 1,
      }}>
        <Typography>
          <b>{projectName}</b> is an application performing quality assessment on 3D RNA
          structures. It reads your uploaded files and processes them using our
          trained models to predict the RMSD score.
        </Typography>

        <Accordion
          expanded={expanded}
          onChange={() => setExpanded((old) => !old)}
          // slots={{ transition: Fade as AccordionSlots['transition'] }}
          // slotProps={{ transition: { timeout: 400 } }}
          sx={{
            '& .MuiAccordion-region': { height: expanded ? 'auto' : 0 },
            '& .MuiAccordionDetails-root': { display: expanded ? 'block' : 'none' },
          }}
        >
          <AccordionSummary expandIcon={<ExpandMoreIcon />}>
            Currently there are 5 computation models available:
          </AccordionSummary>
          <AccordionDetails>
            <ol>
              <li><em>ARES</em> – model trained on ARES dataset, performing well on ARES datasets and one-segment descriptors,</li>
              <li><em>seg1</em> – model trained on one segment descriptors, performing very well on one segment descriptor dataset and yielding satisfactory results on ARES datasets, albeit worse than (1),</li>
              <li><em>seg2</em> (default) – model trained on two segment descriptors, evaluated to be the best performing model overall, although it does not perform well on ARES datasets,</li>
              <li><em>seg3</em> – model trained on three or more segment descriptors, which has poor performance, even on three segment descriptor dataset,</li>
              <li><em>transfer_seg2_ares</em> – model <em>seg2</em> overtrained on ARES data, trying to improve <em>seg2</em>'s performance on ARES data. Unfortunately the resulting model performs very poorly universally on all analyzed datasets.</li>
            </ol>
          </AccordionDetails>
        </Accordion>
        <Typography>
          After you submit your task, simply save the generated URL to see your
          results later on.
        </Typography>
        <Typography>
          This website is free and open to everyone and there is no login
          requirement. Code is licensed under MIT license.
        </Typography>
      </Box>
    </Card>
  );
};

export default ProjectInfo;
