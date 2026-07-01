from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from api.schemas import TopProductResponse, ChannelActivityResponse, MessageSearchResponse, VisualContentResponse
from src.database import get_db
from typing import List

router = APIRouter(prefix="/api")
@router.get("/reports/top-products",
    response_model=List[TopProductResponse],
    tags=["Reports"],
    summary="Top Mentioned Products",
    description="""
Returns the most frequently mentioned pharmaceutical and cosmetic products
identified within Telegram messages.

The endpoint searches message content using a predefined list of product
keywords and returns the products with the highest number of mentions.
""")

def top_products(
    limit: int = Query(10, ge=1,le=100,
        description="Maximum number of products to return."),
    db: Session = Depends(get_db)
):

    query = text("""
        SELECT
            message_text,
            COUNT(*) AS mentions
        FROM raw.fct_messages
        WHERE message_text IS NOT NULL
        GROUP BY message_text
        ORDER BY mentions DESC
        LIMIT :limit
    """)
    try:

        result = db.execute(query, {"limit": limit})

    except SQLAlchemyError:

        raise HTTPException(
            status_code=500,
            detail="Database query failed."
        )
    

    return [
        dict(row._mapping)
        for row in result
    ]

@router.get("/channels/{channel_name}/activity",
    response_model=List[ChannelActivityResponse],
    tags=["Channels"],
    summary="Channel Activity",
    description="""
Returns daily posting activity and average view counts
for the specified Telegram channel.
""",
responses={
        404: {
            "description": "Channel not found."
        },
        500: {
            "description": "Database error."
        }
    }
)
def channel_activity(
    channel_name: str,
    db: Session = Depends(get_db)
):

    query = text("""
        SELECT
            d.full_date,
            COUNT(*) AS posts,
            ROUND(AVG(f.view_count),2) AS average_views
        FROM raw.fct_messages f

        JOIN raw.dim_channels c
            ON f.channel_key = c.channel_key

        JOIN raw.dim_dates d
            ON f.date_key = d.date_key

        WHERE LOWER(c.channel_name)=LOWER(:channel)

        GROUP BY d.full_date

        ORDER BY d.full_date
    """)

 
    try:

           result = db.execute(
        query,
        {"channel": channel_name}
    ).fetchall()

    except SQLAlchemyError:

        raise HTTPException(
            status_code=500,
            detail="Database query failed."
        )
    if not result:
        raise HTTPException(
            status_code=404,
            detail="Channel not found."
        )

    return [
        dict(r._mapping)
        for r in result
    ]

@router.get("/search/messages",
    response_model=List[MessageSearchResponse],
    tags=["Search"],
    summary="Search Messages",
    description="""
Searches Telegram messages for a given keyword
and returns matching messages.
"""
    )
def search_messages(
    query: str = Query(description="Keyword or phrase to search."
    ),
    limit: int = Query(
        20,
        ge=1,
        le=100,
        description="Maximum number of results."),
    db: Session = Depends(get_db)
):

    sql = text("""
        SELECT
            message_id,
            message_text,
            view_count,
            forward_count
        FROM raw.fct_messages

        WHERE
            LOWER(message_text)
            LIKE LOWER(:keyword)

        LIMIT :limit
    """)

    
    try:

          result = db.execute(
        sql,
        {
            "keyword": f"%{query}%",
            "limit": limit
        }
    )

    except SQLAlchemyError:

        raise HTTPException(
            status_code=500,
            detail="Database query failed."
        )
    if not result:
        raise HTTPException(
            status_code=404,
            detail="No matching messages found."
        )
    return [
        dict(row._mapping)
        for row in result
    ]


@router.get("/reports/visual-content",
    response_model=List[VisualContentResponse],
    tags=["Reports"],
    summary="Visual Content Statistics",
    description="""
Returns statistics about image usage across Telegram channels,
including image categories, total image posts,
and average engagement.
""")
def visual_content(
    db: Session = Depends(get_db)
):

    query = text("""
        SELECT
            c.channel_name,

            d.image_category,

            COUNT(*) AS total_posts,

            ROUND(AVG(f.view_count),2)
                AS average_views

        FROM raw.fct_image_detections d

        JOIN raw.dim_channels c

            ON d.channel_key = c.channel_key

        JOIN raw.fct_messages f

            ON d.message_id = f.message_id

        GROUP BY
            c.channel_name,
            d.image_category

        ORDER BY
            c.channel_name,
            total_posts DESC
    """)

    
    try:

         result = db.execute(query)

    except SQLAlchemyError:

        raise HTTPException(
            status_code=500,
            detail="Database query failed."
        )
    return [
        dict(row._mapping)
        for row in result
    ]