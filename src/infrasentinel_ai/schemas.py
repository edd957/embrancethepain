from pydantic import BaseModel, Field


class ServerEvent(BaseModel):
    host_id: str = Field(min_length=3, max_length=128)
    cpu_percent: float = Field(ge=0, le=100)
    memory_percent: float = Field(ge=0, le=100)
    failed_ssh_logins: int = Field(ge=0, le=500)
    successful_ssh_logins: int = Field(ge=0, le=500)
    sudo_commands: int = Field(ge=0, le=500)
    new_user_created: bool
    process_count: int = Field(ge=1, le=5000)
    outbound_connections: int = Field(ge=0, le=10000)
    bytes_out_mb: float = Field(ge=0)
    listening_ports: int = Field(ge=0, le=1000)
    package_install_count: int = Field(ge=0, le=500)
    hour_of_day: int = Field(ge=0, le=23)
    is_weekend: bool


class RuleFinding(BaseModel):
    rule_id: str
    severity: str
    message: str


class ScoreResponse(BaseModel):
    host_id: str
    anomaly_score: float
    risk_score: int
    risk_level: str
    top_signals: list[str]
    findings: list[RuleFinding]


class RetrievalResult(BaseModel):
    title: str
    score: float
    text: str


class AnalysisResponse(BaseModel):
    score: ScoreResponse
    retrieved_playbooks: list[RetrievalResult]
    analyst_summary: str
    recommended_actions: list[str]


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    version: str
