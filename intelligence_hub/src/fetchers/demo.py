from datetime import datetime, timezone

from intelligence_hub.src.models import Item


def demo_items() -> list[Item]:
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    rows = [
        ("AI 与前沿科技", "OpenAI 发布更低成本多模态 agent 工作流示例", "OpenAI 与多模态 agent 降低推理成本，适合个人自动化工具原型。"),
        ("AI 与前沿科技", "开源模型社区优化长上下文推理基准", "Hugging Face 开源模型在长上下文任务上改进，影响内容研究和知识库工作流。"),
        ("AI 与前沿科技", "NVIDIA 新一代推理芯片供应链扩张", "NVIDIA 算力供给变化影响 AI 应用成本、产业公司和投资观察。"),
        ("机器人与具身智能", "Figure AI 展示 humanoid 工厂协作新进展", "humanoid 机器人在真实工厂任务中提升操作臂稳定性，值得持续跟踪。"),
        ("机器人与具身智能", "具身智能仿真数据集开放 beta", "开源仿真数据集可用于机器人学习工具和研究原型。"),
        ("机器人与具身智能", "Tesla Optimus 供应链出现量产信号", "特斯拉机器人量产信号影响硬件、制造和职业机会。"),
        ("Web3 与数字资产", "稳定币支付 API 增长带来新工具机会", "Circle 和 Coinbase 生态出现稳定币 API 工作流需求。"),
        ("Web3 与数字资产", "以太坊 RWA 项目获得机构合作", "Ethereum RWA 资产上链进展影响 DeFi 和合规机会。"),
        ("Web3 与数字资产", "比特币 ETF 资金流变化提示宏观风险偏好", "Bitcoin 与 ETF 资金流可作为数字资产和宏观情绪信号。"),
        ("金融与宏观", "美联储利率路径预期改变市场流动性", "Federal Reserve 利率和美元流动性变化影响风险资产。"),
        ("金融与宏观", "通胀与就业数据分化提高政策不确定性", "宏观就业和通胀信号影响投资、职业和创业窗口。"),
        ("产业与公司", "Microsoft 扩大 AI agent 企业集成", "Microsoft 企业 agent 集成可能改变个人自动化和咨询机会。"),
        ("产业与公司", "Meta 开源模型策略推动应用生态竞争", "Meta 开源模型降低创业和内容生产工具门槛。"),
        ("政策与监管", "SEC 发布数字资产合规新指引", "SEC 监管方向影响 Web3 项目和投资风险控制。"),
        ("个人机会", "AI workflow 开源项目招募贡献者", "开源项目招聘贡献者，适合进入职业/合作机会池并做工具原型。"),
    ]
    return [
        Item(
            title=title,
            url=f"demo://{idx}",
            source_name="demo",
            source_type="demo",
            summary=summary,
            published_at=now,
            topic=topic,
            raw={"demo": True},
        )
        for idx, (topic, title, summary) in enumerate(rows, start=1)
    ]
