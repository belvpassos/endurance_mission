import os
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class MissionControlSmokeTests(unittest.TestCase):
    def run_python(self, script: str) -> str:
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as db_file:
            db_path = db_file.name

        env = os.environ.copy()
        env["DATABASE_URL"] = f"sqlite:///{db_path}"
        env["PYTHONPATH"] = str(PROJECT_ROOT)

        try:
            completed = subprocess.run(
                [sys.executable, "-c", script],
                cwd=PROJECT_ROOT,
                env=env,
                capture_output=True,
                text=True,
                check=True,
            )
            return completed.stdout.strip()
        finally:
            Path(db_path).unlink(missing_ok=True)

    def test_application_boots_and_exposes_core_routes(self):
        output = self.run_python(
            textwrap.dedent(
                """
                from app.main import app
                paths = sorted(route.path for route in app.routes)
                print("/health" in paths)
                print("/mission-control/overview" in paths)
                print("/demo/bootstrap" in paths)
                """
            )
        )
        self.assertEqual(output.splitlines(), ["True", "True", "True"])

    def test_demo_bootstrap_populates_overview(self):
        output = self.run_python(
            textwrap.dedent(
                """
                import app.main
                from app.database import SessionLocal
                from app.routes.missionControl import bootstrap_demo_data, get_mission_control_overview

                db = SessionLocal()
                try:
                    bootstrap_demo_data(db)
                    overview = get_mission_control_overview(db)
                    print(overview.operational_readiness)
                    print(overview.metrics.missions)
                    print(overview.metrics.spacecraft)
                    print(overview.metrics.crew_members)
                    print(overview.latest_snapshot.spacecraft_name)
                    print(len(overview.recent_events))
                    print(len(overview.active_alerts))
                finally:
                    db.close()
                """
            )
        )
        self.assertEqual(
            output.splitlines(),
            ["nominal", "1", "1", "4", "Endurance", "4", "2"],
        )

    def test_demo_bootstrap_creates_richer_dataset(self):
        output = self.run_python(
            textwrap.dedent(
                """
                import app.main
                from app.database import SessionLocal
                from app.models.alertSystem import AlertSystem
                from app.models.groundControlLog import GroundControlLog
                from app.models.missionEvents import MissionEvent
                from app.models.planet import Planet
                from app.models.spacecraftStatus import SpacecraftStatus
                from app.routes.missionControl import bootstrap_demo_data

                db = SessionLocal()
                try:
                    bootstrap_demo_data(db)
                    print(db.query(Planet).count())
                    print(db.query(MissionEvent).count())
                    print(db.query(AlertSystem).count())
                    print(db.query(GroundControlLog).count())
                    print(db.query(SpacecraftStatus).count())
                finally:
                    db.close()
                """
            )
        )
        self.assertEqual(output.splitlines(), ["3", "4", "3", "3", "2"])

    def test_mission_crud_flow(self):
        output = self.run_python(
            textwrap.dedent(
                """
                import app.main
                from datetime import datetime
                from app.database import SessionLocal
                from app.models.mission import Mission as MissionModel
                from app.routes.mission import create_mission, update_mission, delete_mission
                from app.schemas.mission import MissionCreate, MissionUpdate

                db = SessionLocal()
                try:
                    created = create_mission(
                        MissionCreate(name="Ranger Survey", status="planned", start_time=datetime(2067, 5, 1, 9, 0)),
                        db,
                    )
                    updated = update_mission(created.id, MissionUpdate(status="active"), db)
                    deleted = delete_mission(created.id, db)
                    print(created.name)
                    print(updated.status)
                    print(deleted.detail)
                    print(db.query(MissionModel).count())
                finally:
                    db.close()
                """
            )
        )
        self.assertEqual(
            output.splitlines(),
            ["Ranger Survey", "active", "Mission deleted successfully", "0"],
        )

    def test_spacecraft_crud_flow(self):
        output = self.run_python(
            textwrap.dedent(
                """
                import app.main
                from app.database import SessionLocal
                from app.models.spacecraft import Spacecraft as SpacecraftModel
                from app.routes.spacecraft import create_spacecraft, update_spacecraft, delete_spacecraft
                from app.schemas.spacecraft import SpacecraftCreate, SpacecraftUpdate

                db = SessionLocal()
                try:
                    created = create_spacecraft(
                        SpacecraftCreate(
                            name="Ranger-1",
                            registry_code="RNG-01",
                            vehicle_class="Lander",
                            manufacturer="NASA",
                            status="assembly",
                            mission_profile="Atmospheric survey",
                            home_base="Orbital Dock",
                        ),
                        db,
                    )
                    updated = update_spacecraft(created.id, SpacecraftUpdate(status="ready"), db)
                    deleted = delete_spacecraft(created.id, db)
                    print(created.registry_code)
                    print(updated.status)
                    print(deleted.detail)
                    print(db.query(SpacecraftModel).count())
                finally:
                    db.close()
                """
            )
        )
        self.assertEqual(output.splitlines(), ["RNG-01", "ready", "Spacecraft deleted successfully", "0"])

    def test_alert_crud_flow(self):
        output = self.run_python(
            textwrap.dedent(
                """
                import app.main
                from app.database import SessionLocal
                from app.models.alertSystem import AlertSystem as AlertModel
                from app.routes.alertSystem import create_alert, update_alert, delete_alert
                from app.routes.spacecraft import create_spacecraft
                from app.schemas.alertSystem import AlertCreate, AlertType, AlertUpdate
                from app.schemas.spacecraft import SpacecraftCreate

                db = SessionLocal()
                try:
                    spacecraft = create_spacecraft(
                        SpacecraftCreate(
                            name="CASE",
                            registry_code="CASE-01",
                            vehicle_class="Autonomous support unit",
                            manufacturer="NASA",
                            status="operational",
                            mission_profile="Mission support",
                            home_base="Endurance",
                        ),
                        db,
                    )
                    created = create_alert(
                        AlertCreate(
                            system="Guidance",
                            alert_type=AlertType.WARNING,
                            message="Attitude drift approaching threshold.",
                            acknowledged=False,
                            resolved=False,
                            spacecraft_id=spacecraft.id,
                        ),
                        db,
                    )
                    updated = update_alert(created.id, AlertUpdate(acknowledged=True), db)
                    deleted = delete_alert(created.id, db)
                    print(created.system)
                    print(updated.acknowledged)
                    print(deleted.detail)
                    print(db.query(AlertModel).count())
                finally:
                    db.close()
                """
            )
        )
        self.assertEqual(output.splitlines(), ["Guidance", "True", "Alert deleted successfully", "0"])

    def test_ground_control_log_crud_flow(self):
        output = self.run_python(
            textwrap.dedent(
                """
                import app.main
                from app.database import SessionLocal
                from app.models.groundControlLog import GroundControlLog as LogModel
                from app.routes.groundControlLog import create_log, update_log, delete_log
                from app.routes.spacecraft import create_spacecraft
                from app.schemas.groundControlLog import GroundControlLogCreate, GroundControlLogUpdate
                from app.schemas.spacecraft import SpacecraftCreate

                db = SessionLocal()
                try:
                    spacecraft = create_spacecraft(
                        SpacecraftCreate(
                            name="TARS",
                            registry_code="TARS-01",
                            vehicle_class="Autonomous support unit",
                            manufacturer="NASA",
                            status="operational",
                            mission_profile="Crew support",
                            home_base="Endurance",
                        ),
                        db,
                    )
                    created = create_log(
                        GroundControlLogCreate(
                            sender="Mission Control",
                            receiver="TARS",
                            message_type="directive",
                            content="Hold relay alignment.",
                            acknowledged=False,
                            spacecraft_id=spacecraft.id,
                        ),
                        db,
                    )
                    updated = update_log(created.id, GroundControlLogUpdate(acknowledged=True), db)
                    deleted = delete_log(created.id, db)
                    print(created.message_type)
                    print(updated.acknowledged)
                    print(deleted.detail)
                    print(db.query(LogModel).count())
                finally:
                    db.close()
                """
            )
        )
        self.assertEqual(
            output.splitlines(),
            ["directive", "True", "Ground control log deleted successfully", "0"],
        )

    def test_duplicate_spacecraft_registry_returns_error(self):
        output = self.run_python(
            textwrap.dedent(
                """
                import app.main
                from fastapi import HTTPException
                from app.database import SessionLocal
                from app.routes.spacecraft import create_spacecraft
                from app.schemas.spacecraft import SpacecraftCreate

                db = SessionLocal()
                try:
                    payload = SpacecraftCreate(
                        name="Ranger-2",
                        registry_code="DUP-01",
                        vehicle_class="Lander",
                        manufacturer="NASA",
                        status="assembly",
                        mission_profile="Survey",
                        home_base="Hangar",
                    )
                    create_spacecraft(payload, db)
                    try:
                        create_spacecraft(payload, db)
                    except HTTPException as exc:
                        print(exc.status_code)
                        print("Could not create spacecraft" in exc.detail)
                finally:
                    db.close()
                """
            )
        )
        self.assertEqual(output.splitlines(), ["500", "True"])

    def test_not_found_paths_raise_404(self):
        output = self.run_python(
            textwrap.dedent(
                """
                import app.main
                from fastapi import HTTPException
                from app.database import SessionLocal
                from app.routes.mission import update_mission
                from app.routes.spacecraft import delete_spacecraft
                from app.schemas.mission import MissionUpdate

                db = SessionLocal()
                try:
                    for fn, arg in [
                        (lambda: update_mission(999, MissionUpdate(status="lost"), db), "mission"),
                        (lambda: delete_spacecraft(999, db), "spacecraft"),
                    ]:
                        try:
                            fn()
                        except HTTPException as exc:
                            print(arg, exc.status_code)
                finally:
                    db.close()
                """
            )
        )
        self.assertEqual(output.splitlines(), ["mission 404", "spacecraft 404"])

    def test_navigation_crud_flow(self):
        output = self.run_python(
            textwrap.dedent(
                """
                import app.main
                from app.database import SessionLocal
                from app.models.navigationSystem import NavigationSystem as NavigationModel
                from app.routes.navigationSystem import create_navigation, update_navigation, delete_navigation
                from app.routes.spacecraft import create_spacecraft
                from app.schemas.navigationSystem import NavigationStatus, NavigationSystemCreate, NavigationSystemUpdate
                from app.schemas.spacecraft import SpacecraftCreate

                db = SessionLocal()
                try:
                    spacecraft = create_spacecraft(
                        SpacecraftCreate(
                            name="Ranger-Nav",
                            registry_code="NAV-01",
                            vehicle_class="Lander",
                            manufacturer="NASA",
                            status="operational",
                            mission_profile="Navigation test",
                            home_base="Hangar",
                        ),
                        db,
                    )
                    created = create_navigation(
                        NavigationSystemCreate(
                            trajectory="Transfer arc to Miller",
                            course_correction=1,
                            navigation_system_status=NavigationStatus.OPERATIONAL,
                            spacecraft_id=spacecraft.id,
                        ),
                        db,
                    )
                    updated = update_navigation(
                        created.id,
                        NavigationSystemUpdate(course_correction=2),
                        db,
                    )
                    deleted = delete_navigation(created.id, db)
                    print(created.trajectory)
                    print(updated.course_correction)
                    print(deleted.detail)
                    print(db.query(NavigationModel).count())
                finally:
                    db.close()
                """
            )
        )
        self.assertEqual(
            output.splitlines(),
            ["Transfer arc to Miller", "2", "Navigation entry deleted successfully", "0"],
        )

    def test_resource_usage_log_crud_flow(self):
        output = self.run_python(
            textwrap.dedent(
                """
                import app.main
                from app.database import SessionLocal
                from app.models.resourceUsageLog import ResourceUsageLog as ResourceUsageLogModel
                from app.routes.resourceUsageLog import create_log, update_log, delete_log
                from app.routes.spacecraft import create_spacecraft
                from app.schemas.resourceUsageLog import ResourceUsageLogCreate, ResourceUsageLogUpdate
                from app.schemas.spacecraft import SpacecraftCreate

                db = SessionLocal()
                try:
                    spacecraft = create_spacecraft(
                        SpacecraftCreate(
                            name="Logistics-1",
                            registry_code="LOG-01",
                            vehicle_class="Support craft",
                            manufacturer="NASA",
                            status="operational",
                            mission_profile="Consumables tracking",
                            home_base="Orbital Dock",
                        ),
                        db,
                    )
                    created = create_log(
                        ResourceUsageLogCreate(
                            resource_type="oxygen",
                            amount_used=12.5,
                            amount_remaining=87.5,
                            spacecraft_id=spacecraft.id,
                        ),
                        db,
                    )
                    updated = update_log(created.id, ResourceUsageLogUpdate(amount_remaining=80.0), db)
                    deleted = delete_log(created.id, db)
                    print(created.resource_type)
                    print(updated.amount_remaining)
                    print(deleted.detail)
                    print(db.query(ResourceUsageLogModel).count())
                finally:
                    db.close()
                """
            )
        )
        self.assertEqual(
            output.splitlines(),
            ["oxygen", "80.0", "Resource usage log entry deleted successfully", "0"],
        )


if __name__ == "__main__":
    unittest.main()
