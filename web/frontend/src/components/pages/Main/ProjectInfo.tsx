import { Accordion, AccordionDetails, AccordionSummary, Box, Card, Typography } from "@mui/material";
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';

import { styles } from "../../../utils/styles";
import { projectName } from "../../../../config";

const ProjectInfo = () => {
  return (
    <Card sx={styles.mainCard}>
      <Box sx={styles.gaps}>
        <Typography>
          <b>{projectName}</b> is an application performing quality assessment
          on 3D RNA structures. It reads your uploaded files and processes them
          using our trained models to predict the RMSD score.
        </Typography>

        <Typography>
          After you submit your task, simply save the generated URL to see your
          results later on.
        </Typography>

        <Accordion>
          <AccordionSummary expandIcon={<ExpandMoreIcon />}>
            Available computation methods
          </AccordionSummary>
          <AccordionDetails sx={{ ...styles.gaps, my: 2, px: 5 }}>
            <Typography>
              <b>Local analysis</b> involves studying specific regions or
              segments rather than considering entire structure as a whole.
              These specific substructures are called 3D RNA local descriptors.
              In our framework, structural descriptors describe nucleotide
              neighborhood in pre-determined distance of 16 Å.
            </Typography>
            <Typography>
              We provide three specific computational models according to the
              number of segments of generated descriptors:
            </Typography>
            <ul
              style={{
                display: "flex",
                flexDirection: "column",
                gap: 16,
              }}
            >
              <li>
                <i>seg1</i> – one segment descriptors,
              </li>
              <li>
                <i>seg2</i> – two segment descriptors,
              </li>
              <li>
                <i>seg3</i> – three or more segment descriptors.
              </li>
            </ul>

            <Typography>
              <b>Global analysis</b> considers the overall structure of 3D RNA
              molecules. Contrary to local analysis, global analysis provides a
              broader perspective on a macro scale, taking into account
              relationships and features spanning the entirety of 3D RNA
              structure.
            </Typography>
            <Typography>
              For global analysis we provide a single model, <i>ARES</i>, that
              was trained using ARES dataset.
            </Typography>
          </AccordionDetails>
        </Accordion>

        <Accordion>
          <AccordionSummary expandIcon={<ExpandMoreIcon />}>
            Terms of Use & License
          </AccordionSummary>
          <AccordionDetails sx={{ ...styles.gaps, my: 2, px: 5 }}>
            <Typography>
              This website is free and open to everyone and there is no login
              requirement.
            </Typography>
            <Typography>Code is licensed under MIT license.</Typography>
          </AccordionDetails>
        </Accordion>
      </Box>
    </Card>
  );
};

export default ProjectInfo;
