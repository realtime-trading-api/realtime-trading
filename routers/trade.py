"""
거래 라우터 (Trade Router)
- 사용자 자산 상태 조회 및 매수/매도 로직 처리
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from auth import get_current_user
import models, schemas
from .market import manager

router = APIRouter()

@router.get("/user/status")
async def get_status(
    current_price: float,
    user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """사용자 자산 상태 조회 실습"""

    # TODO: db.execute와 select를 사용해 현재 유저의 Portfolio 정보를 조회하세요

    # TODO: 포트폴리오(p) 존재 여부에 따라 보유수량(amount)과 평단가(avg_price)를 변수에 저장하세요 (없으면 0)

    # TODO: 현재가(current_price)를 기준으로 다음 수치를 계산하세요
    # 1. evaluation: 평가 금액 (보유수량 * 현재가)
    # 2. profit: 평가 손익 (평가 금액 - 투자 원금)
    # 힌트: 투자 원금은 (보유수량 * 평단가) 입니다.

    # TODO: 계산된 정보를 바탕으로 다음 키를 가진 딕셔너리를 반환하세요
    # 반환 키: "cash", "holdings", "evaluation", "profit", "total_asset"
    pass


@router.post("/trade/{action}")
async def trade(
    action: str,
    payload: schemas.TradeRequest,
    user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """매수 및 매도 처리 로직 실습"""

    username = user.username
    # TODO: DB에서 해당 유저의 포트폴리오 정보를 조회하세요 (변수명: p)

    if action == "buy":
        # TODO: 총 매수 비용(cost)을 계산하고, 유저 잔액(user.balance)이 부족할 경우 HTTPException(400)을 발생시키세요.

        # TODO: 유저의 잔액에서 매수 비용을 차감하세요.

        # TODO: 포트폴리오 업데이트 로직을 구현하세요.
        # 1. 기존 데이터(p)가 있는 경우: 가중 평균을 이용해 평단가(p.avg_price)를 갱신하고 수량을 더합니다.
        # 2. 기존 데이터가 없는 경우: 새로운 models.Portfolio 객체를 생성(new_p)하고 db.add() 하세요.
        pass

    elif action == "sell":
        # TODO: 매도 가능 여부를 체크하세요. (포트폴리오가 없거나, 보유 수량 < 매도 요청 수량일 경우 400 에러)

        # TODO: 유저의 잔액을 매도 대금만큼 증가시키고, 포트폴리오 수량(p.amount)을 차감하세요.

        # TODO: 수량이 0이 될 경우 db.delete(p)를 호출하여 데이터를 삭제하세요.
        pass

    # TODO: db.commit()으로 변경 사항을 저장하세요.

    # TODO: manager.broadcast를 사용해 전체 사용자에게 거래 알림 메시지를 전송하세요.
    # 메시지 형식: {"type": "trade_news", "msg": f"🔔 {username}님 {action} 완료"}

    return {"msg": "success"}    