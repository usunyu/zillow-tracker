import { useState, useEffect } from 'react';
// firestore
import { collection, query, getDocs, limit, orderBy } from 'firebase/firestore';
import { Helmet } from 'react-helmet-async';
// @mui
import { Grid, Container, Typography } from '@mui/material';
// firebase
import { db } from '../firebase-config';
// sections
import { AppWebsiteVisits } from '../sections/@dashboard/app';

// ----------------------------------------------------------------------

const FETCH_LIMIT = 500;

export default function TrackingPage({ area, title, description }) {
  const [newListingsAndViewsCountData, setNewListingsAndViewsCountData] = useState([]);

  const fetchNewListingsAndViewsCount = async () => {
    const docQuery = query(collection(db, `${area}-new_listings_and_views_count`), orderBy('time'), limit(FETCH_LIMIT));
    const data = await getDocs(docQuery);
    setNewListingsAndViewsCountData([
      ...newListingsAndViewsCountData,
      ...data.docs.map((doc) => ({ ...doc.data(), id: doc.id })),
    ]);
  };

  useEffect(() => {
    fetchNewListingsAndViewsCount();
  }, []);

  const dateLabel = [];
  const newListingsCount = [];
  const avgViewsCount = [];
  for (let i = 0; i < newListingsAndViewsCountData.length; i += 1) {
    const countData = newListingsAndViewsCountData[i];
    dateLabel.push(countData.date);
    newListingsCount.push(countData.new_listings_count);
    const avgViews = Math.round(countData.total_views_count / countData.new_listings_count);
    avgViewsCount.push(avgViews);
  }

  return (
    <>
      <Helmet>
        <title> {title} | Tracking </title>
      </Helmet>

      <Container maxWidth="xl">
        <Typography variant="h4" sx={{ mb: 1 }}>
          {title}
        </Typography>

        <Typography sx={{ color: 'text.secondary', mb: 3 }}>{description}</Typography>

        <Grid container spacing={3}>
          <Grid item xs={12} md={12} lg={12}>
            <AppWebsiteVisits
              title="New listings"
              subheader="New listings in last 7 days"
              units="listings"
              chartLabels={dateLabel}
              chartData={[
                {
                  name: 'New listings',
                  type: 'area',
                  fill: 'gradient',
                  data: newListingsCount,
                },
              ]}
            />
          </Grid>

          <Grid item xs={12} md={12} lg={12}>
            <AppWebsiteVisits
              title="Average views"
              subheader="Average views on new listings last 7 days"
              units="views"
              chartLabels={dateLabel}
              chartData={[
                {
                  name: 'Average views',
                  type: 'area',
                  fill: 'gradient',
                  data: avgViewsCount,
                },
              ]}
            />
          </Grid>
        </Grid>
      </Container>
    </>
  );
}
