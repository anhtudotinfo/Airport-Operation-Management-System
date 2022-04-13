import { useState, useEffect } from "react";
import { useSelector } from "react-redux";
import Typography from "@mui/material/Typography";
import { Grid, Paper, Button, TextField } from "@mui/material";
import { ClipLoader } from "react-spinners";
import axiosInstance from "../components/Axios";

const MyComplaints = () => {
  const [loading, setLoading] = useState(true);
  const [fileAirportComplaint, setFileAirportComplaint] = useState(false);
  const [fileAirlineComplaint, setFileAirlineComplaint] = useState(false);

  const [passenger, setPassenger] = useState({});
  const [airlines, setAirlines] = useState([]);
  const [airportComplaints, setAirportComplaints] = useState([]);
  const [airlineComplaints, setAirlineComplaints] = useState([]);

  const [description, setDescription] = useState(null);
  const [airline, setAirline] = useState(null);

  const { id } = useSelector((state) => state.user);

  useEffect(async () => {
    try {
      const passenger = await axiosInstance.get(`passenger/${id}/`);
      console.log(passenger.data);
      setPassenger(passenger);
    } catch (err) {
      console.log(err);
    }

    try {
      const airport_complaints = await axiosInstance.get(
        `passenger/airport-complaints/${id}/`
      );
      console.log(airport_complaints.data);
      setAirportComplaints(airport_complaints.data);
    } catch (err) {
      console.log(err);
    }

    try {
      const airline_complaints = await axiosInstance.get(
        `passenger/airline-complaints/${id}/`
      );
      console.log(airline_complaints.data);
      setAirlineComplaints(airline_complaints.data);
    } catch (err) {
      console.log(err);
    }

    setLoading(false);
  }, [id]);

  return (
    <>
      {loading ? (
        <Grid item>
          <ClipLoader loading={loading} size={70} color={"#ffffff"} />
        </Grid>
      ) : (
        <Grid
          container
          direction="column"
          justifyContent="flex-start"
          alignItems="flex-start"
          rowSpacing={5}
        >
          <Grid item>
            <Typography variant="h5" fontWeight="bold">
              Your complaints
            </Typography>
          </Grid>
          {!fileAirportComplaint && !fileAirlineComplaint && (
            <Grid
              item
              container
              direction="row"
              justifyContent="flex-start"
              spacing={3}
            >
              <Grid item>
                <Button
                  variant="contained"
                  sx={{ minWidth: "220px" }}
                  onClick={() => setFileAirportComplaint(true)}
                >
                  File Airport Complaint
                </Button>
              </Grid>
              <Grid item>
                <Button
                  variant="contained"
                  sx={{ minWidth: "220px" }}
                  onClick={() => setFileAirlineComplaint(true)}
                >
                  File Airline Complaint
                </Button>
              </Grid>
            </Grid>
          )}
          {fileAirportComplaint && (
            <Grid
              item
              container
              direction="column"
              alignItems="flex-start"
              rowSpacing={3}
            >
              <Grid item>
                <Typography variant="h6">Airport Complaint</Typography>
              </Grid>
              <Grid item xs={12}>
                <TextField
                  label="complaint"
                  multiline
                  variant="outlined"
                  sx={{
                    "& .MuiOutlinedInput-notchedOutline": {
                      borderColor: "white",
                    },
                    "&:hover .MuiOutlinedInput-notchedOutline": {
                      borderColor: "red",
                    },
                    "&.MuiOutlinedInput-notchedOutline.Mui-focused": {
                      borderColor: "red",
                    },
                    "& .MuiButtonBase-root.MuiIconButton-root": {
                      color: "white",
                    },
                    minWidth: 600,
                  }}
                  rows={4}
                  InputLabelProps={{
                    style: { color: "white" },
                  }}
                  onChange={(event) => {
                    setDescription(event.target.value);
                  }}
                />
              </Grid>
              <Grid
                item
                container
                direction="row"
                justifyContent="flex-start"
                spacing={2}
              >
                <Grid item>
                  <Button
                    variant="contained"
                    onClick={() => {
                      setFileAirportComplaint(false);
                      setDescription(null);
                    }}
                  >
                    Cancel
                  </Button>
                </Grid>
                <Grid item>
                  <Button variant="contained">Submit</Button>
                </Grid>
              </Grid>
            </Grid>
          )}
          {fileAirlineComplaint && (
            <Grid
              item
              container
              direction="column"
              alignItems="flex-start"
              rowSpacing={3}
            >
              <Grid item>
                <Typography variant="h6">Airline Complaint</Typography>
              </Grid>
              <Grid item xs={12}>
                <TextField
                  label="complaint"
                  multiline
                  variant="outlined"
                  sx={{
                    "& .MuiOutlinedInput-notchedOutline": {
                      borderColor: "white",
                    },
                    "&:hover .MuiOutlinedInput-notchedOutline": {
                      borderColor: "red",
                    },
                    "&.MuiOutlinedInput-notchedOutline.Mui-focused": {
                      borderColor: "red",
                    },
                    "& .MuiButtonBase-root.MuiIconButton-root": {
                      color: "white",
                    },
                    minWidth: 600,
                  }}
                  rows={4}
                  InputLabelProps={{
                    style: { color: "white" },
                  }}
                  onChange={(event) => {
                    setDescription(event.target.value);
                  }}
                />
              </Grid>
              <Grid
                item
                container
                direction="row"
                justifyContent="flex-start"
                spacing={2}
              >
                <Grid item>
                  <Button
                    variant="contained"
                    onClick={() => {
                      setFileAirlineComplaint(false);
                      setDescription(null);
                    }}
                  >
                    Cancel
                  </Button>
                </Grid>
                <Grid item>
                  <Button variant="contained">Submit</Button>
                </Grid>
              </Grid>
            </Grid>
          )}
          <Grid
            item
            container
            direction="column"
            alignItems="flex-start"
            rowSpacing={2}
          >
            <Grid item>
              <Typography variant="h6">Airport Complaints</Typography>
            </Grid>
            {airportComplaints.length === 0 ? (
              <Grid item ml="20px">
                <Typography>No airport complaints</Typography>
              </Grid>
            ) : (
              <Grid item container direction="column" ml="20px">
                {airportComplaints.map((complaint) => {
                  return <Grid item>{complaint.description}</Grid>;
                })}
              </Grid>
            )}
          </Grid>
          <Grid
            item
            container
            direction="column"
            alignItems="flex-start"
            rowSpacing={2}
          >
            <Grid item>
              <Typography variant="h6">Airline Complaints</Typography>
            </Grid>
            {airlineComplaints.length === 0 ? (
              <Grid item ml="20px">
                <Typography>No airline complaints</Typography>
              </Grid>
            ) : (
              <Grid item container direction="column" ml="20px">
                {airlineComplaints.map((complaint) => {
                  return <Grid item>{complaint.description}</Grid>;
                })}
              </Grid>
            )}
          </Grid>
        </Grid>
      )}
    </>
  );
};

export default MyComplaints;
