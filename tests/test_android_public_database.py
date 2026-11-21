from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANDROID = ROOT / "android/app/src/main/java/org/assayflux/molecularis"


def test_public_database_adapters_are_bounded_and_allowlisted() -> None:
    client = (ANDROID / "PublicDatabaseClient.kt").read_text()
    assert '"eutils.ncbi.nlm.nih.gov"' in client
    assert '"rest.uniprot.org"' in client
    assert '"files.rcsb.org"' in client
    assert "instanceFollowRedirects = false" in client
    assert "CONNECT_TIMEOUT_MS" in client and "READ_TIMEOUT_MS" in client
    assert "MAX_METADATA_BYTES" in client
    assert "MAX_SEQUENCE_BYTES" in client
    assert "MAX_STRUCTURE_BYTES" in client
    assert "searchNcbiSequence" in client
    assert "searchNcbiGeneLinkedSequences" in client
    assert "fetchUniProtFasta" in client
    assert "fetchRcsbMmcif" in client


def test_public_reference_payloads_are_encrypted_and_deletable() -> None:
    store = (ANDROID / "PublicRecordStore.kt").read_text()
    assert "LocalCrypto.ensureChunkedFileHeader" in store
    assert "LocalCrypto.appendEncryptedChunk" in store
    assert "LocalCrypto.decryptChunkedFile" in store
    assert "kinetics-public-record:" in store
    assert "fun delete(id: String)" in store
    assert "fun loadRecord(id: String)" in store
    assert "public_records" in store


def test_public_sequences_and_structures_reach_existing_engines() -> None:
    card = (ANDROID / "PublicDatabaseCard.kt").read_text()
    viewer = (ANDROID / "StructureViewer.kt").read_text()
    ui = (ANDROID / "MolecularisUi.kt").read_text()
    assert 'callAttr("analyze_fasta", fetched.content)' in card
    assert "store.saveAnalysis(saved.id, json)" in card
    assert "onStructureFetched(fetched)" in card
    assert "searchGeneLinks(hit, \"nuccore\")" in card
    assert "searchGeneLinks(hit, \"protein\")" in card
    assert "store.loadRecord(saved.id)" in card
    assert "Reanalyse" in card
    assert "Saved RCSB structure reopened from encrypted local storage." in card
    assert 'callAttr("prepare_structure_viewer_import", fetched.content, "mmcif")' in viewer
    assert "PublicDatabaseCard(onStructureFetched = { publicStructureRecord = it })" in ui
    assert "StructureViewerPreview(publicRecord = publicStructureRecord)" in ui


def test_public_database_never_submits_imported_patient_data() -> None:
    client = (ANDROID / "PublicDatabaseClient.kt").read_text()
    card = (ANDROID / "PublicDatabaseCard.kt").read_text()
    assert "never submit patient sequences" in client
    assert "Imported patient data is never uploaded" in card
    assert "contentResolver" not in card


def test_public_reference_cache_has_explicit_quota_and_clear_all() -> None:
    store = (ANDROID / "PublicRecordStore.kt").read_text()
    assert "MAX_CACHE_BYTES = 200L * 1024 * 1024" in store
    assert "MAX_RECORDS = 50" in store
    assert "enforceCacheQuota(protectedId = id)" in store
    assert "ORDER BY saved_at ASC" in store
    assert "fun totalBytes(): Long" in store
    assert "fun recordCount(): Int" in store
    assert "fun deleteAll()" in store
    card = (ANDROID / "PublicDatabaseCard.kt").read_text()
    assert "store.deleteAll()" in card
    assert "Clear saved public records?" in card
