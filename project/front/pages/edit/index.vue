<script setup>
import { ref, onMounted } from 'vue'

const activeTab = ref('brandClient')

// 데이터 상태
const brandClients = ref([])
const projects = ref([])
const works = ref([])
const categories = ref([])
const inquiries = ref([])

// 폼 상태
const formBc = ref({ name: '', subtitle: '' })
const formProject = ref({ title: '', subtitle: '', client: '' })
const formCategory = ref({ name: '', subtitle: '', order: 0, is_vertical: false })
const formWork = ref({ 
  title: '', 
  category: '', 
  youtube_link: '', 
  content: '',
  status: 'IN_PROGRESS', 
  is_visible: true,
  thumbnail_url: '' // 유튜브 썸네일 미리보기용
})

// 카테고리 인라인 수정 상태
const editingCategoryId = ref(null)
const editingCategoryData = ref({ id: null, name: '', subtitle: '', order: 0, is_vertical: false })

// 브랜드 클라이언트 인라인 수정 상태
const editingBrandClientId = ref(null)
const editingBrandClientData = ref({ id: null, name: '', subtitle: '' })

// 프로젝트 인라인 수정 상태
const editingProjectId = ref(null)
const editingProjectData = ref({ id: null, title: '', subtitle: '', client: '' })

// 유튜브 검색 상태
const searchQuery = ref('')
const searchResults = ref([])
const isSearching = ref(false)

// 비디오 플레이어 상태
const playingVideoId = ref('')

// 데이터 불러오기 함수
const loadBrandClients = async () => {
  try {
    brandClients.value = await $fetch('http://127.0.0.1:8000/work/admin/brandclients/')
  } catch (e) { console.error(e) }
}
const loadProjects = async () => {
  try {
    projects.value = await $fetch('http://127.0.0.1:8000/work/admin/projects/')
  } catch (e) { console.error(e) }
}
const loadWorks = async () => {
  try {
    works.value = await $fetch('http://127.0.0.1:8000/work/admin/works/')
  } catch (e) { console.error(e) }
}
const loadCategories = async () => {
  try {
    categories.value = await $fetch('http://127.0.0.1:8000/work/admin/categories/')
  } catch (e) { console.error(e) }
}
const loadInquiries = async () => {
  try {
    inquiries.value = await $fetch('http://127.0.0.1:8000/work/inquiries/')
  } catch (e) { console.error(e) }
}

onMounted(() => {
  loadBrandClients()
  loadProjects()
  loadWorks()
  loadCategories()
  loadInquiries()
})

// 추가 함수들
const addBrandClient = async () => {
  if (!formBc.value.name) return alert('브랜드명을 입력해주세요.')
  try {
    await $fetch('http://127.0.0.1:8000/work/admin/brandclients/', {
      method: 'POST',
      body: { 
        name: formBc.value.name,
        subtitle: formBc.value.subtitle || ''
      }
    })
    formBc.value = { name: '', subtitle: '' }
    alert('브랜드 클라이언트가 추가되었습니다.')
    loadBrandClients()
  } catch (e) {
    console.error(e)
    alert('추가 실패')
  }
}

const deleteBrandClient = async (id) => {
  if (!confirm('정말 삭제하시겠습니까?')) return
  await $fetch(`http://127.0.0.1:8000/work/admin/brandclients/${id}/`, { method: 'DELETE' })
  loadBrandClients()
}

const startEditingBrandClient = (bc) => {
  editingBrandClientId.value = bc.id
  editingBrandClientData.value = { 
    id: bc.id, 
    name: bc.name, 
    subtitle: bc.subtitle 
  }
}

const cancelEditingBrandClient = () => {
  editingBrandClientId.value = null
}

const saveBrandClient = async () => {
  try {
    await $fetch(`http://127.0.0.1:8000/work/admin/brandclients/${editingBrandClientData.value.id}/`, {
      method: 'PATCH',
      body: { 
        name: editingBrandClientData.value.name,
        subtitle: editingBrandClientData.value.subtitle || ''
      }
    })
    alert('브랜드가 성공적으로 수정되었습니다.')
    editingBrandClientId.value = null
    loadBrandClients()
  } catch (e) {
    console.error(e)
    alert('브랜드 수정에 실패했습니다.')
    loadBrandClients()
  }
}

// 카테고리 추가/삭제
const addCategory = async () => {
  if (!formCategory.value.name) return alert('카테고리명을 입력해주세요.')
  try {
    await $fetch('http://127.0.0.1:8000/work/admin/categories/', {
      method: 'POST',
      body: { 
        name: formCategory.value.name,
        subtitle: formCategory.value.subtitle || '',
        order: formCategory.value.order || 0,
        is_vertical: formCategory.value.is_vertical || false
      }
    })
    formCategory.value = { name: '', subtitle: '', order: 0, is_vertical: false }
    alert('카테고리가 성공적으로 추가되었습니다.')
    loadCategories()
  } catch (e) {
    console.error(e)
    alert('추가 실패')
  }
}

const startEditingCategory = (cat) => {
  editingCategoryId.value = cat.id
  editingCategoryData.value = { 
    id: cat.id, 
    name: cat.name, 
    subtitle: cat.subtitle,
    order: cat.order, 
    is_vertical: cat.is_vertical 
  }
}

const cancelEditingCategory = () => {
  editingCategoryId.value = null
}

const saveCategory = async () => {
  try {
    await $fetch(`http://127.0.0.1:8000/work/admin/categories/${editingCategoryData.value.id}/`, {
      method: 'PATCH',
      body: { 
        name: editingCategoryData.value.name,
        subtitle: editingCategoryData.value.subtitle || '',
        order: editingCategoryData.value.order,
        is_vertical: editingCategoryData.value.is_vertical
      }
    })
    alert('카테고리가 성공적으로 수정되었습니다.')
    editingCategoryId.value = null
    loadCategories()
  } catch (e) {
    console.error(e)
    alert('카테고리 수정에 실패했습니다.')
    loadCategories()
  }
}

const deleteCategory = async (id) => {
  if (!confirm('정말 삭제하시겠습니까? 관련 영상의 카테고리가 비워질 수 있습니다.')) return
  await $fetch(`http://127.0.0.1:8000/work/admin/categories/${id}/`, { method: 'DELETE' })
  loadCategories()
}

const addProject = async () => {
  if (!formProject.value.title) return alert('프로젝트명을 입력해주세요.')
  try {
    await $fetch('http://127.0.0.1:8000/work/admin/projects/', {
      method: 'POST',
      body: { 
        title: formProject.value.title,
        subtitle: formProject.value.subtitle || '',
        client: formProject.value.client || null 
      }
    })
    formProject.value = { title: '', subtitle: '', client: '' }
    alert('납품 프로젝트가 추가되었습니다.')
    loadProjects()
  } catch (e) {
    console.error(e)
    alert('추가 실패')
  }
}

const deleteProject = async (id) => {
  if (!confirm('정말 삭제하시겠습니까?')) return
  await $fetch(`http://127.0.0.1:8000/work/admin/projects/${id}/`, { method: 'DELETE' })
  loadProjects()
}

const startEditingProject = (p) => {
  editingProjectId.value = p.id
  editingProjectData.value = { 
    id: p.id, 
    title: p.title, 
    subtitle: p.subtitle,
    client: p.client 
  }
}

const cancelEditingProject = () => {
  editingProjectId.value = null
}

const saveProject = async () => {
  try {
    await $fetch(`http://127.0.0.1:8000/work/admin/projects/${editingProjectData.value.id}/`, {
      method: 'PATCH',
      body: { 
        title: editingProjectData.value.title,
        subtitle: editingProjectData.value.subtitle || '',
        client: editingProjectData.value.client || null
      }
    })
    alert('프로젝트가 성공적으로 수정되었습니다.')
    editingProjectId.value = null
    loadProjects()
  } catch (e) {
    console.error(e)
    alert('프로젝트 수정에 실패했습니다.')
    loadProjects()
  }
}

// 유튜브 정보 불러오기 API 연동
const fetchYoutubeInfo = async () => {
  if (!formWork.value.youtube_link) {
    return alert('유튜브 링크를 먼저 입력해주세요.')
  }
  try {
    const data = await $fetch(`http://127.0.0.1:8000/work/admin/youtube-info/?url=${encodeURIComponent(formWork.value.youtube_link)}`)
    if (data.title) {
      formWork.value.title = data.title
      formWork.value.thumbnail_url = data.thumbnail_url
      alert('유튜브 정보를 성공적으로 불러왔습니다.')
    }
  } catch (e) {
    console.error(e)
    alert('유튜브 정보를 불러오는데 실패했습니다. 올바른 링크인지 확인해주세요.')
  }
}

const searchYoutube = async () => {
  if (!searchQuery.value) return alert('검색어를 입력해주세요.')
  isSearching.value = true
  searchResults.value = []
  
  try {
    const data = await $fetch(`http://127.0.0.1:8000/work/admin/youtube-search/?q=${encodeURIComponent(searchQuery.value)}`)
    if (data.error) {
      alert(data.error)
    } else {
      searchResults.value = data
      if (data.length === 0) alert('검색 결과가 없습니다.')
    }
  } catch (e) {
    console.error(e)
    alert(e.response?._data?.error || '검색에 실패했습니다.')
  } finally {
    isSearching.value = false
  }
}

const selectYoutubeResult = (result) => {
  formWork.value.title = result.title
  formWork.value.youtube_link = result.youtube_link
  formWork.value.thumbnail_url = result.thumbnail_url
  searchResults.value = [] // 선택 후 목록 닫기
  searchQuery.value = ''
}

// 최종 영상(Work) 추가
const addWork = async () => {
  if (!formWork.value.title) return alert('작품명(제목)을 입력해주세요. (유튜브 정보 불러오기를 추천합니다)')
  if (!formWork.value.category) return alert('카테고리를 선택해주세요.')
  
  try {
    await $fetch('http://127.0.0.1:8000/work/admin/works/', {
      method: 'POST',
      body: { 
        title: formWork.value.title,
        youtube_link: formWork.value.youtube_link || null,
        category: formWork.value.category,
        content: formWork.value.content || '',
        status: formWork.value.status,
        is_visible: formWork.value.is_visible
      }
    })
    // 초기화
    formWork.value = { title: '', category: '', youtube_link: '', content: '', status: 'IN_PROGRESS', is_visible: true, thumbnail_url: '' }
    alert('최종 영상이 성공적으로 추가되었습니다.')
    loadWorks()
  } catch (e) {
    console.error(e)
    alert('추가 실패')
  }
}

const deleteWork = async (id) => {
  if (!confirm('정말 삭제하시겠습니까?')) return
  await $fetch(`http://127.0.0.1:8000/work/admin/works/${id}/`, { method: 'DELETE' })
  loadWorks()
}

// 영상 상태/공개여부 실시간 수정
const updateWorkStatus = async (work) => {
  try {
    await $fetch(`http://127.0.0.1:8000/work/admin/works/${work.id}/`, {
      method: 'PATCH',
      body: { status: work.status }
    })
  } catch (e) {
    console.error(e)
    alert('상태 업데이트에 실패했습니다.')
    loadWorks()
  }
}

const updateWorkVisibility = async (work) => {
  try {
    await $fetch(`http://127.0.0.1:8000/work/admin/works/${work.id}/`, {
      method: 'PATCH',
      body: { is_visible: work.is_visible }
    })
  } catch (e) {
    console.error(e)
    alert('공개 여부 업데이트에 실패했습니다.')
    loadWorks()
  }
}

// 영상 바로 시청하기 (모달 띄우기)
const playVideo = (url) => {
  if (!url) return
  const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/
  const match = url.match(regExp)
  if (match && match[2].length === 11) {
    playingVideoId.value = match[2]
  } else {
    window.open(url, '_blank') // 파싱 실패시 새창으로 열기
  }
}

const closeVideo = () => {
  playingVideoId.value = ''
}

// 문의 내역 삭제
const deleteInquiry = async (id) => {
  if (!confirm('정말 삭제하시겠습니까?')) return
  await $fetch(`http://127.0.0.1:8000/work/inquiries/${id}/`, { method: 'DELETE' })
  loadInquiries()
}

// 문의 읽음 처리
const toggleInquiryRead = async (inq) => {
  try {
    await $fetch(`http://127.0.0.1:8000/work/inquiries/${inq.id}/`, {
      method: 'PATCH',
      body: { is_read: !inq.is_read }
    })
    loadInquiries()
  } catch (e) {
    console.error(e)
  }
}

// 문의 상태 변경 (미접수, 처리 중, 처리 완료)
const updateInquiryStatus = async (inq) => {
  try {
    await $fetch(`http://127.0.0.1:8000/work/inquiries/${inq.id}/`, {
      method: 'PATCH',
      body: { status: inq.status }
    })
  } catch (e) {
    console.error(e)
    alert('상태 업데이트에 실패했습니다.')
    loadInquiries()
  }
}
</script>

<template>
  <div class="profile-layout edit-layout">
    <div class="profile-grid">
      <!-- 사이드바 -->
      <aside class="dashboard-panel">
        <h2 class="panel-title">데이터 관리</h2>
        <ul class="admin-menu">
          <li :class="{ active: activeTab === 'brandClient' }" @click="activeTab = 'brandClient'">브랜드 클라이언트</li>
          <li :class="{ active: activeTab === 'project' }" @click="activeTab = 'project'">납품 프로젝트</li>
          <li :class="{ active: activeTab === 'category' }" @click="activeTab = 'category'">카테고리 관리</li>
          <li :class="{ active: activeTab === 'work' }" @click="activeTab = 'work'">최종 영상 (Works)</li>
          <li :class="{ active: activeTab === 'inquiry' }" @click="activeTab = 'inquiry'">문의 내역 관리</li>
        </ul>
      </aside>

      <!-- 메인 폼 영역 -->
      <main class="profile-panel">
        <!-- 브랜드 클라이언트 탭 -->
        <div v-if="activeTab === 'brandClient'">
          <h2 class="panel-title">브랜드 클라이언트 관리</h2>
          
          <div class="section">
            <h3>새 브랜드 추가</h3>
            <div class="form-row">
              <div class="form-group flex-1">
                <input v-model="formBc.name" type="text" placeholder="브랜드명 입력" />
              </div>
              <div class="form-group flex-1">
                <input v-model="formBc.subtitle" type="text" placeholder="소제목(부가설명) 입력 (선택)" />
              </div>
              <button class="btn-submit" @click="addBrandClient">추가하기</button>
            </div>
          </div>

          <div class="section">
            <h3>등록된 브랜드 목록</h3>
            <table class="data-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>브랜드명</th>
                  <th>부가설명</th>
                  <th>관리</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="bc in brandClients" :key="bc.id">
                  <template v-if="editingBrandClientId === bc.id">
                    <td>{{ bc.id }}</td>
                    <td>
                      <input type="text" v-model="editingBrandClientData.name" style="width: 100%; padding: 6px; border: 1px solid #ddd; border-radius: 4px;" />
                    </td>
                    <td>
                      <input type="text" v-model="editingBrandClientData.subtitle" style="width: 100%; padding: 6px; border: 1px solid #ddd; border-radius: 4px;" />
                    </td>
                    <td>
                      <button class="btn-submit" @click="saveBrandClient" style="padding: 6px 12px; font-size: 12px; margin-right: 5px; height: auto;">저장</button>
                      <button class="btn-delete" @click="cancelEditingBrandClient" style="padding: 6px 12px; font-size: 12px; height: auto; background-color: #888;">취소</button>
                    </td>
                  </template>
                  <template v-else>
                    <td>{{ bc.id }}</td>
                    <td>{{ bc.name }}</td>
                    <td>{{ bc.subtitle || '-' }}</td>
                    <td>
                      <button class="btn-submit" @click="startEditingBrandClient(bc)" style="padding: 6px 12px; font-size: 12px; margin-right: 5px; height: auto; background-color: #f39c12;">수정</button>
                      <button class="btn-delete" @click="deleteBrandClient(bc.id)" style="padding: 6px 12px; font-size: 12px; height: auto;">삭제</button>
                    </td>
                  </template>
                </tr>
                <tr v-if="brandClients.length === 0">
                  <td colspan="4" class="text-center">등록된 데이터가 없습니다.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- 납품 프로젝트 탭 -->
        <div v-if="activeTab === 'project'">
          <h2 class="panel-title">납품 프로젝트 관리</h2>
          
          <div class="section">
            <h3>새 프로젝트 추가</h3>
            <div class="form-row">
              <div class="form-group flex-2">
                <input v-model="formProject.title" type="text" placeholder="프로젝트명 입력" />
              </div>
              <div class="form-group flex-2">
                <input v-model="formProject.subtitle" type="text" placeholder="소제목(부가설명) 입력 (선택)" />
              </div>
              <div class="form-group flex-1">
                <select v-model="formProject.client">
                  <option value="">클라이언트 선택 (선택사항)</option>
                  <option v-for="bc in brandClients" :key="bc.id" :value="bc.id">{{ bc.name }}</option>
                </select>
              </div>
              <button class="btn-submit" @click="addProject">추가하기</button>
            </div>
          </div>

          <div class="section">
            <h3>등록된 프로젝트 목록</h3>
            <table class="data-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>프로젝트명</th>
                  <th>부가설명</th>
                  <th>클라이언트</th>
                  <th>관리</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="p in projects" :key="p.id">
                  <template v-if="editingProjectId === p.id">
                    <td>{{ p.id }}</td>
                    <td>
                      <input type="text" v-model="editingProjectData.title" style="width: 100%; padding: 6px; border: 1px solid #ddd; border-radius: 4px;" />
                    </td>
                    <td>
                      <input type="text" v-model="editingProjectData.subtitle" style="width: 100%; padding: 6px; border: 1px solid #ddd; border-radius: 4px;" />
                    </td>
                    <td>
                      <select v-model="editingProjectData.client" style="width: 100%; padding: 6px; border: 1px solid #ddd; border-radius: 4px;">
                        <option value="">선택 안함</option>
                        <option v-for="bc in brandClients" :key="bc.id" :value="bc.id">{{ bc.name }}</option>
                      </select>
                    </td>
                    <td>
                      <button class="btn-submit" @click="saveProject" style="padding: 6px 12px; font-size: 12px; margin-right: 5px; height: auto;">저장</button>
                      <button class="btn-delete" @click="cancelEditingProject" style="padding: 6px 12px; font-size: 12px; height: auto; background-color: #888;">취소</button>
                    </td>
                  </template>
                  <template v-else>
                    <td>{{ p.id }}</td>
                    <td>{{ p.title }}</td>
                    <td>{{ p.subtitle || '-' }}</td>
                    <td>{{ p.client_name || '-' }}</td>
                    <td>
                      <button class="btn-submit" @click="startEditingProject(p)" style="padding: 6px 12px; font-size: 12px; margin-right: 5px; height: auto; background-color: #f39c12;">수정</button>
                      <button class="btn-delete" @click="deleteProject(p.id)" style="padding: 6px 12px; font-size: 12px; height: auto;">삭제</button>
                    </td>
                  </template>
                </tr>
                <tr v-if="projects.length === 0">
                  <td colspan="5" class="text-center">등록된 데이터가 없습니다.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- 카테고리 탭 -->
        <div v-if="activeTab === 'category'">
          <h2 class="panel-title">카테고리 관리</h2>
          
          <div class="section">
            <h3>새 카테고리 추가</h3>
            <div class="form-row" style="align-items: flex-end;">
              <div class="form-group flex-2">
                <label>카테고리명 *</label>
                <input v-model="formCategory.name" type="text" placeholder="예: 브랜드 필름" />
              </div>
              <div class="form-group flex-2">
                <label>소제목 (선택)</label>
                <input v-model="formCategory.subtitle" type="text" placeholder="예: 광고 · TVCF" />
              </div>
              <div class="form-group flex-1">
                <label>노출 순서</label>
                <input v-model="formCategory.order" type="number" placeholder="0" style="width:100%; padding:12px 15px; border:1px solid #ddd; border-radius:6px;" />
              </div>
              <div class="form-group flex-1" style="display:flex; align-items:center; gap:8px; padding-bottom: 12px;">
                <input type="checkbox" id="isVertical" v-model="formCategory.is_vertical" />
                <label for="isVertical" style="margin:0; cursor:pointer;">세로형(쇼츠) 여부</label>
              </div>
              <button class="btn-submit" @click="addCategory" style="margin-bottom: 2px;">추가하기</button>
            </div>
          </div>

          <div class="section">
            <h3>등록된 카테고리 목록</h3>
            <table class="data-table">
              <thead>
                <tr>
                  <th>순서(Order)</th>
                  <th>카테고리명</th>
                  <th>소제목</th>
                  <th>형태</th>
                  <th>관리</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="cat in categories" :key="cat.id">
                  <template v-if="editingCategoryId === cat.id">
                    <td>
                      <input type="number" v-model="editingCategoryData.order" style="width: 60px; padding: 6px; text-align: center; border: 1px solid #ddd; border-radius: 4px;" />
                    </td>
                    <td>
                      <input type="text" v-model="editingCategoryData.name" style="width: 100%; max-width: 150px; padding: 6px; border: 1px solid #ddd; border-radius: 4px;" />
                    </td>
                    <td>
                      <input type="text" v-model="editingCategoryData.subtitle" style="width: 100%; max-width: 150px; padding: 6px; border: 1px solid #ddd; border-radius: 4px;" />
                    </td>
                    <td>
                      <div style="display:flex; justify-content:center; align-items:center; height:100%;">
                        <input type="checkbox" v-model="editingCategoryData.is_vertical" style="cursor:pointer; width:16px; height:16px;" />
                      </div>
                    </td>
                    <td>
                      <button class="btn-submit" @click="saveCategory" style="padding: 6px 12px; font-size: 12px; margin-right: 5px; height: auto;">저장</button>
                      <button class="btn-delete" @click="cancelEditingCategory" style="padding: 6px 12px; font-size: 12px; height: auto; background-color: #888;">취소</button>
                    </td>
                  </template>
                  <template v-else>
                    <td>{{ cat.order }}</td>
                    <td>{{ cat.name }}</td>
                    <td>{{ cat.subtitle || '-' }}</td>
                    <td>{{ cat.is_vertical ? '세로형(쇼츠)' : '가로형' }}</td>
                    <td>
                      <button class="btn-submit" @click="startEditingCategory(cat)" style="padding: 6px 12px; font-size: 12px; margin-right: 5px; height: auto; background-color: #f39c12;">수정</button>
                      <button class="btn-delete" @click="deleteCategory(cat.id)" style="padding: 6px 12px; font-size: 12px; height: auto;">삭제</button>
                    </td>
                  </template>
                </tr>
                <tr v-if="categories.length === 0">
                  <td colspan="5" class="text-center">등록된 데이터가 없습니다.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- 최종 영상 탭 -->
        <div v-if="activeTab === 'work'">
          <h2 class="panel-title">최종 영상 (Work) 관리</h2>
          
          <div class="section">
            <h3>새 영상 포트폴리오 추가</h3>
            
            <!-- 유튜브 URL 또는 검색 입력부 -->
            <div class="form-row" style="margin-bottom: 15px; align-items: flex-end;">
              <div class="form-group flex-1">
                <label>유튜브 영상 링크</label>
                <div style="display:flex; gap:10px;">
                  <input v-model="formWork.youtube_link" type="text" placeholder="https://www.youtube.com/watch?v=..." />
                  <button class="btn-submit" @click="fetchYoutubeInfo" style="background-color: #f00;">링크로 불러오기</button>
                </div>
              </div>
              <div class="form-group flex-1" style="position: relative;">
                <label>또는 유튜브 검색</label>
                <div style="display:flex; gap:10px;">
                  <input v-model="searchQuery" type="text" placeholder="검색어 입력 후 Enter" @keyup.enter="searchYoutube" />
                  <button class="btn-submit" @click="searchYoutube" style="background-color: #333;">{{ isSearching ? '검색중...' : '검색' }}</button>
                </div>
                
                <!-- 검색 결과 드롭다운 -->
                <div v-if="searchResults.length > 0" class="search-results-dropdown">
                  <div class="search-close-btn" @click="searchResults = []">✕ 닫기</div>
                  <div v-for="res in searchResults" :key="res.video_id" class="search-result-item" @click="selectYoutubeResult(res)">
                    <img :src="res.thumbnail_url" alt="thumbnail" class="result-thumb" />
                    <div class="result-title">{{ res.title }}</div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 미리보기 썸네일 -->
            <div v-if="formWork.thumbnail_url" style="margin-bottom: 15px;">
              <img :src="formWork.thumbnail_url" alt="미리보기" style="max-height: 150px; border-radius: 8px; border: 1px solid #ddd;" />
            </div>

            <!-- 세부 입력 폼 -->
            <div class="form-row" style="margin-bottom: 15px;">
              <div class="form-group flex-2">
                <label>작품명(제목) *</label>
                <input v-model="formWork.title" type="text" placeholder="작품명 입력 (유튜브 연동 시 자동 입력됨)" />
              </div>
              <div class="form-group flex-1">
                <label>카테고리 *</label>
                <select v-model="formWork.category">
                  <option value="">카테고리 선택</option>
                  <option v-for="cat in categories" :key="cat.id" :value="cat.id">{{ cat.name }}</option>
                </select>
              </div>
            </div>

            <div class="form-row" style="margin-bottom: 15px;">
              <div class="form-group flex-1">
                <label>게시글 내용 (선택)</label>
                <textarea v-model="formWork.content" rows="3" placeholder="간략한 설명이나 참여 스태프 정보 등을 적어주세요"></textarea>
              </div>
            </div>

            <div class="form-row" style="margin-bottom: 15px;">
              <div class="form-group flex-1">
                <label>진행 상태</label>
                <select v-model="formWork.status">
                  <option value="IN_PROGRESS">작업중 (In Progress)</option>
                  <option value="COMPLETED">완료됨 (Completed)</option>
                </select>
              </div>
              <div class="form-group flex-1" style="display: flex; align-items: center; gap: 10px; margin-top: 25px;">
                <input type="checkbox" id="isVisible" v-model="formWork.is_visible" />
                <label for="isVisible" style="margin:0; font-weight:600; cursor:pointer;">홈페이지 공개 여부</label>
              </div>
              <div class="flex-1" style="text-align:right; margin-top: 20px;">
                <button class="btn-submit" @click="addWork">영상 추가하기</button>
              </div>
            </div>
          </div>

          <div class="section">
            <h3>등록된 영상 목록 (총 {{ works.length }}개)</h3>
            <table class="data-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>카테고리</th>
                  <th>작품명</th>
                  <th>상태</th>
                  <th>공개</th>
                  <th>관리</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="w in works" :key="w.id">
                  <td>{{ w.id }}</td>
                  <td>{{ w.category_name || '-' }}</td>
                  <td>
                    <span v-if="w.youtube_link" @click="playVideo(w.youtube_link)" style="color:#1a3ae0; font-weight:600; cursor:pointer; text-decoration:underline;">
                      ▶ {{ w.title }}
                    </span>
                    <span v-else>{{ w.title }}</span>
                  </td>
                  <td>
                    <select v-model="w.status" @change="updateWorkStatus(w)" style="padding: 5px; font-size: 12px; font-weight: bold; width: 100px;" :style="{ color: w.status === 'COMPLETED' ? '#27ae60' : '#f39c12', borderColor: w.status === 'COMPLETED' ? '#27ae60' : '#f39c12' }">
                      <option value="IN_PROGRESS" style="color: #f39c12;">작업중</option>
                      <option value="COMPLETED" style="color: #27ae60;">완료됨</option>
                    </select>
                  </td>
                  <td>
                    <div style="display:flex; justify-content:center; align-items:center; height:100%;">
                      <input type="checkbox" v-model="w.is_visible" @change="updateWorkVisibility(w)" style="cursor:pointer; width:16px; height:16px;" />
                    </div>
                  </td>
                  <td><button class="btn-delete" @click="deleteWork(w.id)">삭제</button></td>
                </tr>
                <tr v-if="works.length === 0">
                  <td colspan="6" class="text-center">등록된 데이터가 없습니다.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- 문의 내역 탭 -->
        <div v-if="activeTab === 'inquiry'">
          <h2 class="panel-title">문의 내역 관리</h2>
          
          <div class="section">
            <h3>접수된 문의 목록 (총 {{ inquiries.length }}건)</h3>
            <table class="data-table">
              <thead>
                <tr>
                  <th>확인여부</th>
                  <th>등록일</th>
                  <th>제목 / 연락처 / 카테고리</th>
                  <th>상세 내용</th>
                  <th>관리</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="inq in inquiries" :key="inq.id">
                  <td style="text-align:center;">
                    <button 
                      @click="toggleInquiryRead(inq)"
                      style="border:none; padding:4px 8px; border-radius:4px; font-size:12px; cursor:pointer;"
                      :style="{ backgroundColor: inq.is_read ? '#eee' : '#1a3ae0', color: inq.is_read ? '#666' : '#fff' }"
                    >
                      {{ inq.is_read ? '읽음' : '새 문의' }}
                    </button>
                  </td>
                  <td>{{ new Date(inq.created_at).toLocaleDateString() }}</td>
                  <td>
                    <div style="font-weight:bold; margin-bottom:4px;">{{ inq.title }}</div>
                    <div style="font-size:12px; color:#666;">
                      {{ inq.name }} ({{ inq.company || '소속없음' }})<br>
                      {{ inq.phone }} | {{ inq.email || '이메일없음' }}<br>
                      [{{ inq.category || '카테고리없음' }}] 예산: {{ inq.budget }}
                    </div>
                  </td>
                  <td>
                    <div style="font-size:13px; max-width:300px; white-space:pre-wrap;">{{ inq.details || '-' }}</div>
                  </td>
                  <td>
                    <div style="display:flex; align-items:center; gap:8px;">
                      <select v-model="inq.status" @change="updateInquiryStatus(inq)" style="padding: 4px; font-size: 12px; font-weight: bold; width: 100px; border-radius: 4px;" :style="{ color: inq.status === 'COMPLETED' ? '#27ae60' : inq.status === 'IN_PROGRESS' ? '#f39c12' : '#e74c3c', borderColor: inq.status === 'COMPLETED' ? '#27ae60' : inq.status === 'IN_PROGRESS' ? '#f39c12' : '#e74c3c' }">
                        <option value="UNPROCESSED" style="color: #e74c3c;">미접수</option>
                        <option value="IN_PROGRESS" style="color: #f39c12;">처리 중</option>
                        <option value="COMPLETED" style="color: #27ae60;">처리 완료</option>
                      </select>
                      <button class="btn-delete" @click="deleteInquiry(inq.id)">삭제</button>
                    </div>
                  </td>
                </tr>
                <tr v-if="inquiries.length === 0">
                  <td colspan="5" class="text-center">접수된 문의 내역이 없습니다.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

      </main>
    </div>

    <!-- 비디오 모달 (영상 바로 시청) -->
    <div v-if="playingVideoId" class="video-modal-overlay" @click="closeVideo">
      <div class="video-modal-content" @click.stop>
        <button class="video-modal-close" @click="closeVideo">✕ 닫기</button>
        <div class="video-responsive-wrap">
          <iframe 
            :src="`https://www.youtube.com/embed/${playingVideoId}?autoplay=1`" 
            frameborder="0" 
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
            allowfullscreen>
          </iframe>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Profile 뷰와 유사한 레이아웃 스타일 */
.profile-layout {
  max-width: 1000px;
  margin: 60px auto;
  padding: 0 20px;
}

.edit-layout {
  max-width: 1200px; /* 에디터는 가로로 좀 더 넓게 */
}

.profile-grid {
  display: grid;
  grid-template-columns: 250px 1fr;
  gap: 30px;
}

@media (max-width: 768px) {
  .profile-grid {
    grid-template-columns: 1fr;
  }
}

.dashboard-panel, .profile-panel {
  background-color: white;
  border-radius: 8px;
  padding: 40px 30px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
  border: 1px solid #eaeaea;
}

.panel-title {
  margin-bottom: 30px;
  font-weight: 700;
  color: #222;
  font-size: 20px;
  border-bottom: 2px solid #111;
  padding-bottom: 15px;
}

/* 관리자 메뉴 사이드바 */
.admin-menu {
  list-style: none;
  padding: 0;
  margin: 0;
}

.admin-menu li {
  padding: 15px 20px;
  margin-bottom: 10px;
  background-color: #fafafa;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  color: #555;
  transition: all 0.2s;
  border: 1px solid #eee;
}

.admin-menu li:hover {
  background-color: #f0f0f0;
}

.admin-menu li.active {
  background-color: #1a3ae0;
  color: #fff;
  border-color: #1a3ae0;
}

/* 폼 스타일 */
.section {
  margin-bottom: 40px;
}

.section h3 {
  font-size: 16px;
  font-weight: 700;
  color: #111;
  margin-bottom: 15px;
}

.form-row {
  display: flex;
  gap: 15px;
  align-items: center;
}

.form-group {
  margin-bottom: 0;
}

.flex-1 { flex: 1; }
.flex-2 { flex: 2; }

.form-group label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: #555;
  margin-bottom: 5px;
}

input[type="text"], select, textarea {
  width: 100%;
  padding: 12px 15px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  font-family: inherit;
}

.btn-submit {
  padding: 12px 25px;
  background-color: #111;
  color: white;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  white-space: nowrap;
}

.btn-submit:hover {
  background-color: #1a3ae0;
}

/* 테이블 스타일 */
.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th, .data-table td {
  padding: 12px 15px;
  border-bottom: 1px solid #eee;
  text-align: left;
  font-size: 14px;
}

.data-table th {
  background-color: #fafafa;
  font-weight: 600;
  color: #444;
}

.btn-delete {
  padding: 6px 12px;
  background-color: #ff4757;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 12px;
  cursor: pointer;
}

.btn-delete:hover {
  background-color: #ff6b81;
}

.text-center {
  text-align: center;
}

/* 검색 결과 드롭다운 */
.search-results-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  width: 100%;
  background: white;
  border: 1px solid #ddd;
  border-radius: 6px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
  z-index: 100;
  max-height: 350px;
  overflow-y: auto;
  margin-top: 5px;
}

.search-close-btn {
  text-align: right;
  padding: 8px 15px;
  font-size: 12px;
  color: #888;
  cursor: pointer;
  border-bottom: 1px solid #eee;
}
.search-close-btn:hover { color: #f00; }

.search-result-item {
  display: flex;
  gap: 12px;
  padding: 12px 15px;
  border-bottom: 1px solid #f5f5f5;
  cursor: pointer;
  align-items: center;
}

.search-result-item:hover {
  background-color: #f9f9f9;
}

.result-thumb {
  width: 100px;
  height: 56px;
  object-fit: cover;
  border-radius: 4px;
}

.result-title {
  font-size: 13px;
  color: #333;
  line-height: 1.4;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

/* 비디오 모달 */
.video-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.85);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.video-modal-content {
  position: relative;
  width: 90%;
  max-width: 1000px;
  background: #000;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0,0,0,0.5);
}

.video-modal-close {
  position: absolute;
  top: -40px;
  right: 0;
  background: none;
  border: none;
  color: #fff;
  font-size: 16px;
  cursor: pointer;
}

.video-responsive-wrap {
  position: relative;
  padding-bottom: 56.25%; /* 16:9 비율 */
  height: 0;
  overflow: hidden;
}

.video-responsive-wrap iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
</style>
