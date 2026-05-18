# Model Card

## Model Details

- Name: InfraSentinel Server Anomaly Detector
- Version: 0.1.0
- Model type: Isolation Forest
- Framework: scikit-learn
- Intended use: Defensive infrastructure anomaly detection and alert triage

## Intended Use

The model identifies unusual server telemetry patterns and supports human analysts with explainable risk scoring. It is designed for engineering evaluation, demos, and architecture review.

It should not be used as a sole production control without validation on real approved telemetry, monitoring, calibration, access control, and human oversight.

## Inputs

- CPU and memory utilization
- SSH login activity
- Sudo command volume
- Local user creation indicator
- Process count
- Outbound connection volume
- Outbound data transfer volume
- Listening ports
- Package installation count
- Hour and weekend context

## Outputs

- Normalized anomaly score
- Risk score
- Risk level
- Top suspicious signals
- Deterministic security findings

## Limitations

- Training data is synthetic.
- The default model is unsupervised and should be calibrated against real traffic before production use.
- The model should complement, not replace, existing security controls.
- Rule findings are intentionally conservative and defensive.

## Monitoring

Use drift reports to detect changes in server behavior. Production deployments should add alert quality metrics, false-positive review, incident outcomes, and host-group-specific baselines.
