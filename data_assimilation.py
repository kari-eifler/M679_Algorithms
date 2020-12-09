#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Data Assimilation on temperature readings

@author: Kari_Eifler
"""
import pandas as pd
import numpy as np

# Optimization
import cvxpy as cp



def compute_monthly_temperature_means(df, begin_year=None, end_year=None):
    """
    Computes the mean temperature of every column (month) in the passed DataFrame, df,
    in the range [begin_year, end_year], inclusive.  The passed DataFrame is expected
    to contain a MultiIndex in which the first level is the station ID, and the second
    level contains the set of years during which the corresponding station was in 
    service.  The mean temperatures are given per column for all stations operating
    wholly or partially within the given range [begin_year, end_year].
    begin_year - The first year to be included in the mean.  If begin_year is None
        then the first available year in the data is used.  All stations in service
        during this year or after (but not after end_year) are inlcuded in the means.
    end_year - The last year to be included in the mean.  If end_year is None
        then the last available year in the data is used.  All stations in service
        during this year or before (but not before begin_year) are inlcuded in the means.
    Returns - A Pandas Series containing the mean temperatures of the columns in 
        the DataFrame over the specified range of years.  The series name property will
        be set to 'monthly mean'.
    """
    if begin_year is not None and end_year is not None:
        pd2 = df.loc[pd.IndexSlice[:, range(begin_year, end_year+1)], :]
    elif begin_year is None and end_year is not None:
        pd2 = df.loc[pd.IndexSlice[:, range(0, end_year+1)], :]
    elif begin_year is not None and end_year is None:
        pd2 = df.loc[pd.IndexSlice[:, range(begin_year, 2021)], :]
    else: #both are None
        pd2 = df
    
    return pd2.mean(axis = 0)


def compute_annual_temperature_means(df, begin_year=None, end_year=None):
    """
    Computes the mean annual temperature of all stations in every year in the passed 
    DataFrame, df, in the range [begin_year, end_year], inclusive.  The passed DataFrame 
    is expected to contain a MultiIndex in which the first level is the station ID, and 
    the second level contains the set of years during which the corresponding station 
    was in service.  The mean annual temperature is computed in two steps:
      1) The monthly mean is computed from all stations operating in each year with the
         passed range [begin_year, end_year].  The result of this step alone is a 
         DataFrame where each row correpsonds to a single year, and each column 
         corresponds to a single month.  The values stored in the DataFrame are the the
         mean temperatures from all stations operating during the given month and year.
      2) The annual mean is computed by the naive mean of all rows in the result of the 
         first step.
    begin_year - The first year to be included in the mean.  If begin_year is None
        then the first available year in the data is used.  All stations in service
        during this year or after (but not after end_year) are inlcuded in the means.
    end_year - The last year to be included in the mean.  If end_year is None
        then the last available year in the data is used.  All stations in service
        during this year or before (but not before begin_year) are inlcuded in the means.
    Returns - A Pandas Series containing the mean temperatures of the columns in 
        the DataFrame over the specified range of years.  The year indices in the returned
        Series should be sorted in ascending order (small to large). The series name 
        property will be set to 'annual mean'.
    """
    pd2 = compute_monthly_temperature_means(df, begin_year, end_year)
    return pd2.mean()


def get_operating_stations_by_year(df, begin_year=None, end_year=None):
    """
    Creates and returns a Pandas Index containing the unique set of station id's
    for all stations operating between begin_year and end_year inclusive.  The 
    included stations are those that have at least on non-NaN entry during at 
    least one month in any year (not necessarily all years) within the passed 
    range of years.
    df - A Pandas DataFrame with MultiIndex containing the station ID and years of
        operation, and columns containing the mean temperature recorded at each
        station during the month (column) and year (row).
    begin_year - The first year to be included.  If begin_year is None then the 
        first available year in the data is used.  All stations in service during 
        this year or after (but not after end_year) are inlcuded in the set of 
        returned station ids.
    end_year - The last year to be included.  If end_year is None then the last 
        available year in the data is used.  All stations in service during this 
        year or before (but not before begin_year) are inlcuded in the set of 
        returned station ids.
    Returns - A Pandas Index containing the ids of all operating stations in the
        given range of years.  The name property of the Index set will be set to 
        'ID'.
    """
    if begin_year is None:
        begin_year = 0
    if end_year is None:
        end_year = 2021
    
    df2 = df.loc[(slice(None), range(begin_year,end_year+1)),:]
    
    df3 = df2.dropna(thresh=1) #at least one month is not NaN
    
    stations = df3.index.get_level_values(0)
    
    return stations
    

def get_operating_stations_by_month(df, month, begin_year=None, end_year=None):
    """
    Creates and returns a Pandas Index containing the unique set of station id's
    for all stations operating between begin_year and end_year inclusive, and have 
    valid (non-NaN) data during the given month (not necessarily in all years).  
    df - A Pandas DataFrame with MultiIndex containing the station ID and years of
        operation, and columns containing the mean temperature recorded at each
        station during the month (column) and year (row).
    month - A string from the set of column names (months) in df.  Only stations
        with valid (non-NaN) data during this month will be included in the returned
        Pandas Index.
    begin_year - The first year to be included.  If begin_year is None then the 
        first available year in the data is used.  Stations in service during 
        this year or after (but not after end_year) with valid data during month
        are inlcuded in the set of returned station ids.
    end_year - The last year to be included.  If end_year is None then the last 
        available year in the data is used.  Stations in service during this year 
        or before (but not before begin_year) with valid data during month are
        inlcuded in the set of returned station ids.
    Returns - A Pandas Index containing the ids of all operating stations in the
        given range of years with valid data in month.  The name property of the 
        Index set will be set to 'ID'.
    """
    if begin_year is None:
        begin_year = 0
    if end_year is None:
        end_year = 2021
    
    df2 = df.loc[(slice(None), range(begin_year,end_year+1)),:]
    df3 = df2[month]
    df3 = df3.dropna()
    
    stations = df3.index.get_level_values(0)
    
    return stations


def get_station_locations(inv_df, stations=None):
    """
    Returns the positions of the set of passed stations.
    as Pandas Series of the 
    columnes named lat_colname and lon_colname from the DataFrame df for the
    set of stations in operation between begin_year and end_year, inclusive.  
    inv_df - A Pandas DataFrame containing the latitude and longitude 
        (columns), and indexed by the station ID's.
    stations - A Pandas Series of station ID's that should be found in inv_df
        and their positions returned. If stations is None then all station
        locations in the inventory should be returned.
    Returns - A tuple containing the latitudes and longitudes of the set of
        stations found in both stations and inv_df.  Both the latitudes and
        longitudes are represented as Pandas Series.  The series name 
        property for the returned Series will be set to their respective 
        column names in inv_df.
    """
    df2 = inv_df.T
    
    if stations is not None:
        df2 = df2[stations]
    
    df3 = df2.T #transpose
    
    latitudes = df3['lat']
    longitudes = df3['lon']
    
    return[latitudes, longitudes]
    


def get_valid_station_temps_by_month(df, month, year):
    """
    Creates and returns a np.array containing the valid temperatures from all
    stations operating during year, and have valid (non-NaN) data during the given
    month.  The order of the temperature values in the returned array matches the
    order of station ids given by get_operating_stations_by_month for the same month
    and year (single year, not range of years).
    df - A Pandas DataFrame with MultiIndex containing the station ID and years of
        operation, and columns containing the mean temperature recorded at each
        station during the month (column) and year (row).
    month - A string from the set of column names (months) in df.  Only stations
        with valid (non-NaN) data during this month will be included in the array 
        of temperatures returned.
    year - Numeric value representing a year from df.  Stations in service during 
        this year with valid data during month are inlcuded in the set of 
        temperatures returned.
    Returns - A np.array containing the temperatures of all operating stations in 
    the given year with valid data in month.
    """
    df2 = gistemp_df.loc[(slice(None), range(year,year+1)), month]
    df3 = df2.dropna()
    
    station_temps = df3.to_numpy()
    
    return station_temps

    
def get_valid_station_temps_by_year(df, year):
    """
    Creates and returns a np.array containing the mean annual temperatures from all
    stations operating during year.  The order of the annual mean temperature in 
    the returned array matches the order of station ids given by 
    get_operating_stations_by_year for the same year (single year, not range of
    years).
    df - A Pandas DataFrame with MultiIndex containing the station ID and years of
        operation, and columns containing the mean temperature recorded at each
        station during the month (column) and year (row).
    year - Numeric value representing a year from df.  Stations in service during 
        this year with valid data are inlcuded in the set of annual means returned.
    Returns - A np.array containing the annual mean temperatures from all operating
        stations in the given year.
    """
    df2 = df.loc[(slice(None), range(year,year+1)), :]
    
    df3 = df2.dropna(thresh=1) #at least one month is not NaN
    
    
    df4 = df3.T
    df4.columns = df4.columns.droplevel(1)
    
    df5 = df4.mean(axis=0)
    station_temps = df5.to_numpy()
    return station_temps







