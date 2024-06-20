"""
Chroma Web Viewer

This script provides a web interface for viewing collections in Chroma DB using Streamlit.

Usage:
    streamlit run chroma_db_viewer.py

Author: [Purushothaman](https://github.com/purushothaman06)
"""

import chromadb as db
import pandas as pd
import streamlit as st
from urllib.parse import urlparse, ParseResult

pd.set_option("display.max_columns", 4)


def create_client(host: str, port: int) -> db.HttpClient:
    """
    Creates a new HttpClient object with the given host and port.

    Args:
        host: The hostname of the server.
        port: The port number of the server.

    Returns:
        HttpClient: A new HttpClient object.
    """
    return db.HttpClient(host, port)


def style_dataframe(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Styles a DataFrame by highlighting the maximum value in each column.

    Args:
        dataframe: The DataFrame to style.

    Returns:
        pd.Styler: The styled DataFrame.
    """
    return dataframe.style.highlight_max(
        axis=0, props="background-color: white; color: black; border-color: black"
    )


def parse_database_url(db_url: str) -> ParseResult:
    """
    Parses the database URL to extract the host and port.

    Args:
        db_url: The database URL.

    Returns:
        ParseResult: The parsed URL components.
    """
    return urlparse(db_url)


def connect_and_list_collections(client: db.HttpClient) -> None:
    """
    Connects to the database and lists all collections.

    Args:
        client: The HttpClient object.

    Returns:
        None
    """
    try:
        collections = client.list_collections()

        for collection in collections:
            data = collection.get()

            # Assuming the data contains lists of ids, embeddings, metadata, and documents
            ids = data.get("ids", [])
            embeddings = data.get("embeddings", [])
            metadata = data.get("metadatas", [])
            documents = data.get("documents", [])

            # Create a DataFrame from the retrieved data
            df = pd.DataFrame(
                {
                    "ids": ids,
                    "embeddings": embeddings,
                    "metadata": metadata,
                    "documents": documents,
                }
            )

            # Style the DataFrame
            styled_df = style_dataframe(df)

            # Display the collection name and its styled data table
            st.markdown(f"### Collection: **{collection.name}**")
            st.dataframe(styled_df)
    except Exception as e:
        st.error(f"Error listing collections: {e}")


def view_chroma_db() -> None:
    """
    Main function to view Chroma DB collections in Streamlit.

    Returns:
        None
    """
    st.sidebar.markdown("## Enter Database URL")

    # Input field for the database URL in the sidebar
    db_url = st.sidebar.text_input("Database URL")
    connect_button = st.sidebar.button("Connect")

    if connect_button and db_url:
        parsed_url = parse_database_url(db_url)
        host = parsed_url.hostname
        port = parsed_url.port

        if host and port:
            st.markdown(f"### Connecting to {host}:{port}")
            client = create_client(host, port)
            connect_and_list_collections(client)
        else:
            st.error("Invalid URL. Please enter a valid database URL.")


if __name__ == "__main__":
    view_chroma_db()
