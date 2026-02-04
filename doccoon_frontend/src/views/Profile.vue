<template>
    <div
        class="min-h-screen bg-[var(--bg-color)] text-[var(--text-color)] flex"
    >
        <!-- Sidebar -->
        <aside
            class="h-screen flex flex-col border-r border-[var(--border-color)] bg-[var(--section-alt-bg)] transition-all duration-200 overflow-hidden shrink-0"
            :style="{ width: sidebarCollapsed ? '0px' : `${sidebarWidth}px` }"
        >
            <div class="flex flex-col h-full min-w-[240px]">
                <!-- User Section -->
                <div class="p-3 border-b border-[var(--border-color)]">
                    <div class="relative" ref="userDropdownRef">
                        <button
                            class="w-full flex items-center gap-2.5 px-2.5 py-2 rounded-md hover:bg-[var(--border-color)] transition-colors duration-150 cursor-pointer"
                            @click="userDropdownOpen = !userDropdownOpen"
                        >
                            <span
                                class="w-7 h-7 rounded-md bg-primary text-white text-xs font-semibold flex items-center justify-center shrink-0"
                            >
                                {{ initials }}
                            </span>
                            <span
                                class="flex-1 text-left text-sm font-medium truncate"
                            >
                                {{ user?.full_name || "Workspace" }}
                            </span>
                            <BaseIcon
                                name="chevron-down"
                                :size="14"
                                class="opacity-50 transition-transform duration-200"
                                :class="{ 'rotate-180': userDropdownOpen }"
                            />
                        </button>

                        <!-- User Dropdown -->
                        <Transition
                            enter-active-class="transition duration-100 ease-out"
                            enter-from-class="opacity-0 -translate-y-1"
                            enter-to-class="opacity-100 translate-y-0"
                            leave-active-class="transition duration-75 ease-in"
                            leave-from-class="opacity-100 translate-y-0"
                            leave-to-class="opacity-0 -translate-y-1"
                        >
                            <div
                                v-if="userDropdownOpen"
                                class="absolute left-0 right-0 top-full mt-1 bg-[var(--page-bg)] border border-[var(--border-color)] rounded-md shadow-lg z-50 overflow-hidden"
                            >
                                <div
                                    class="px-3 py-2.5 border-b border-[var(--border-color)]"
                                >
                                    <div class="text-sm font-medium truncate">
                                        {{ user?.full_name || "User" }}
                                    </div>
                                    <div
                                        class="text-xs opacity-50 truncate mt-0.5"
                                    >
                                        {{ user?.email || "" }}
                                    </div>
                                </div>
                                <div class="p-1">
                                    <button
                                        class="w-full flex items-center gap-2.5 px-2.5 py-2 text-sm rounded hover:bg-[var(--border-color)] transition-colors cursor-pointer"
                                        @click="openSettings"
                                    >
                                        <BaseIcon name="settings" :size="15" />
                                        Settings
                                    </button>
                                    <button
                                        class="w-full flex items-center gap-2.5 px-2.5 py-2 text-sm rounded hover:bg-[var(--border-color)] transition-colors cursor-pointer"
                                        @click="toggleTheme"
                                    >
                                        <BaseIcon
                                            :name="isDarkTheme ? 'sun' : 'moon'"
                                            :size="15"
                                        />
                                        {{
                                            isDarkTheme
                                                ? "Light mode"
                                                : "Dark mode"
                                        }}
                                    </button>
                                    <div
                                        class="h-px bg-[var(--border-color)] my-1"
                                    />
                                    <button
                                        class="w-full flex items-center gap-2.5 px-2.5 py-2 text-sm rounded hover:bg-[var(--border-color)] transition-colors text-[var(--btn-delete-bg)] cursor-pointer"
                                        @click="handleLogout"
                                    >
                                        <BaseIcon name="log-out" :size="15" />
                                        Log out
                                    </button>
                                </div>
                            </div>
                        </Transition>
                    </div>
                </div>

                <!-- Search -->
                <div class="px-3 pt-3">
                    <div class="relative">
                        <BaseIcon
                            name="search"
                            :size="14"
                            class="absolute left-2.5 top-1/2 -translate-y-1/2 opacity-40"
                        />
                        <input
                            v-model="searchQuery"
                            type="text"
                            placeholder="Search books..."
                            class="w-full pl-8 pr-3 py-1.5 text-sm bg-[var(--bg-color)] border border-[var(--border-color)] rounded-md outline-none transition-colors focus:border-primary"
                        />
                    </div>
                </div>

                <!-- New Book Button -->
                <div class="px-3 py-3">
                    <button
                        class="w-full flex items-center justify-center gap-2 px-3 py-2 bg-primary text-white text-sm font-medium rounded-md hover:opacity-90 transition-opacity cursor-pointer"
                        @click="openCreateModal"
                    >
                        <BaseIcon name="plus" :size="15" />
                        New Book
                    </button>
                </div>

                <!-- Books Section -->
                <div class="flex-1 flex flex-col overflow-hidden">
                    <div
                        class="px-4 py-2 flex items-center justify-between text-xs font-medium opacity-50 uppercase tracking-wide"
                    >
                        <span>Books</span>
                        <span>{{ books.length }}</span>
                    </div>

                    <!-- Loading -->
                    <div v-if="loading" class="px-3 py-4 space-y-2">
                        <div
                            class="h-8 bg-[var(--border-color)] rounded animate-pulse"
                        />
                        <div
                            class="h-8 bg-[var(--border-color)] rounded animate-pulse w-4/5"
                        />
                        <div
                            class="h-8 bg-[var(--border-color)] rounded animate-pulse"
                        />
                    </div>

                    <!-- Empty -->
                    <div
                        v-else-if="filteredBooks.length === 0"
                        class="px-4 py-6 text-center text-sm opacity-50"
                    >
                        {{
                            searchQuery
                                ? "No books match your search"
                                : "No books yet"
                        }}
                    </div>

                    <!-- Book Tree -->
                    <div v-else class="flex-1 overflow-y-auto px-2 pb-3">
                        <div
                            v-for="book in filteredBooks"
                            :key="book.id"
                            class="mb-0.5"
                        >
                            <!-- Book Row -->
                            <div
                                class="flex items-center gap-1 px-2 py-1.5 rounded-md cursor-pointer transition-colors group"
                                :class="
                                    selectedBookId === book.id
                                        ? 'bg-primary/10'
                                        : 'hover:bg-[var(--border-color)]'
                                "
                                @click="selectBook(book)"
                                @dblclick="openBookInEditor(book.id)"
                                @contextmenu.prevent="
                                    openContextMenu($event, 'book', book)
                                "
                            >
                                <button
                                    class="w-5 h-5 flex items-center justify-center rounded hover:bg-[var(--border-color)] transition-colors cursor-pointer"
                                    @click.stop="toggleBookExpanded(book.id)"
                                >
                                    <BaseIcon
                                        name="chevron-right"
                                        :size="12"
                                        class="transition-transform duration-150"
                                        :class="{
                                            'rotate-90': expandedBooks.has(
                                                book.id,
                                            ),
                                        }"
                                    />
                                </button>
                                <BaseIcon
                                    name="book"
                                    :size="15"
                                    class="opacity-60 shrink-0"
                                />
                                <span
                                    class="flex-1 text-sm truncate"
                                    :class="
                                        selectedBookId === book.id
                                            ? 'font-medium'
                                            : ''
                                    "
                                >
                                    {{ book.title }}
                                </span>
                                <span
                                    v-if="book.status === 'Published'"
                                    class="w-1.5 h-1.5 rounded-full bg-primary shrink-0"
                                    title="Published"
                                />
                            </div>

                            <!-- Pages -->
                            <div
                                v-if="
                                    expandedBooks.has(book.id) &&
                                    bookPages[book.id]
                                "
                                class="ml-5 border-l border-[var(--border-color)]"
                            >
                                <div
                                    v-for="page in bookPages[book.id]"
                                    :key="page.id"
                                    class="flex items-center gap-2 px-3 py-1.5 ml-1 rounded-md cursor-pointer transition-colors"
                                    :class="
                                        selectedPageId === page.id
                                            ? 'bg-primary/10'
                                            : 'hover:bg-[var(--border-color)]'
                                    "
                                    @click.stop="selectPage(book, page)"
                                    @dblclick="
                                        openPageInEditor(
                                            book.id,
                                            page.page_number,
                                        )
                                    "
                                >
                                    <BaseIcon
                                        name="file-text"
                                        :size="14"
                                        class="opacity-50 shrink-0"
                                    />
                                    <span class="text-sm truncate">
                                        Page {{ page.page_number }}
                                    </span>
                                </div>
                                <div
                                    v-if="bookPages[book.id]?.length === 0"
                                    class="px-3 py-1.5 ml-1 text-sm opacity-40"
                                >
                                    No pages
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Footer Links -->
                <div
                    class="p-2 border-t border-[var(--border-color)] flex flex-col gap-0.5"
                >
                    <router-link
                        to="/"
                        class="flex items-center gap-2.5 px-2.5 py-2 text-sm rounded-md opacity-70 hover:opacity-100 hover:bg-[var(--border-color)] transition-all no-underline text-[var(--text-color)] cursor-pointer"
                    >
                        <BaseIcon name="home" :size="15" />
                        Home
                    </router-link>
                    <router-link
                        to="/docs"
                        class="flex items-center gap-2.5 px-2.5 py-2 text-sm rounded-md opacity-70 hover:opacity-100 hover:bg-[var(--border-color)] transition-all no-underline text-[var(--text-color)] cursor-pointer"
                    >
                        <BaseIcon name="book-open" :size="15" />
                        Documentation
                    </router-link>
                </div>
            </div>

            <!-- Resize Handle -->
            <div
                class="absolute right-0 top-0 bottom-0 w-1 cursor-col-resize hover:bg-primary/50 transition-colors"
                @mousedown="startResize"
            />
        </aside>

        <!-- Sidebar Toggle -->
        <button
            v-if="sidebarCollapsed"
            class="fixed left-3 top-3 z-50 w-8 h-8 flex items-center justify-center bg-[var(--section-alt-bg)] border border-[var(--border-color)] rounded-md hover:bg-[var(--border-color)] transition-colors cursor-pointer"
            @click="sidebarCollapsed = false"
        >
            <BaseIcon name="panel-left" :size="16" />
        </button>

        <!-- Main Content -->
        <main class="flex-1 flex flex-col min-w-0 overflow-hidden">
            <!-- Top Bar -->
            <header
                class="h-14 px-4 flex items-center gap-3 border-b border-[var(--border-color)] bg-[var(--bg-color)] shrink-0"
            >
                <button
                    class="w-8 h-8 flex items-center justify-center rounded-md hover:bg-[var(--section-alt-bg)] transition-colors opacity-70 hover:opacity-100 cursor-pointer"
                    @click="sidebarCollapsed = !sidebarCollapsed"
                >
                    <BaseIcon name="panel-left" :size="16" />
                </button>

                <div class="flex-1 flex items-center gap-2 text-sm">
                    <span class="opacity-50">Workspace</span>
                    <template v-if="selectedBook">
                        <BaseIcon
                            name="chevron-right"
                            :size="12"
                            class="opacity-30"
                        />
                        <span class="font-medium">{{
                            selectedBook.title
                        }}</span>
                    </template>
                </div>

                <NotificationDropdown />
            </header>

            <!-- Content -->
            <div class="flex-1 overflow-y-auto">
                <!-- Welcome View -->
                <div v-if="!selectedBook" class="max-w-4xl mx-auto px-6 py-10">
                    <div class="mb-10">
                        <h1 class="text-2xl font-semibold mb-2">
                            Welcome back, {{ user?.first_name || "there" }}
                        </h1>
                        <p class="text-sm opacity-60">
                            You have {{ books.length }}
                            {{ books.length === 1 ? "book" : "books" }} with
                            {{ totalPages }}
                            {{ totalPages === 1 ? "page" : "pages" }} in your
                            workspace.
                        </p>
                    </div>

                    <!-- Stats -->
                    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-10">
                        <div
                            class="p-4 bg-[var(--section-alt-bg)] border border-[var(--border-color)] rounded-lg"
                        >
                            <div class="text-2xl font-semibold">
                                {{ books.length }}
                            </div>
                            <div class="text-xs opacity-50 mt-1">Books</div>
                        </div>
                        <div
                            class="p-4 bg-[var(--section-alt-bg)] border border-[var(--border-color)] rounded-lg"
                        >
                            <div class="text-2xl font-semibold">
                                {{ totalPages }}
                            </div>
                            <div class="text-xs opacity-50 mt-1">Pages</div>
                        </div>
                        <div
                            class="p-4 bg-[var(--section-alt-bg)] border border-[var(--border-color)] rounded-lg"
                        >
                            <div class="text-2xl font-semibold">
                                {{ totalImages }}
                            </div>
                            <div class="text-xs opacity-50 mt-1">Images</div>
                        </div>
                        <div
                            class="p-4 bg-[var(--section-alt-bg)] border border-[var(--border-color)] rounded-lg"
                        >
                            <div class="text-2xl font-semibold">
                                {{ publishedCount }}
                            </div>
                            <div class="text-xs opacity-50 mt-1">Published</div>
                        </div>
                    </div>

                    <!-- Recent Books -->
                    <div>
                        <h2 class="text-base font-medium mb-4">Recent Books</h2>

                        <div
                            v-if="recentBooks.length === 0"
                            class="text-center py-12 border border-dashed border-[var(--border-color)] rounded-lg"
                        >
                            <BaseIcon
                                name="book"
                                :size="32"
                                class="opacity-20 mx-auto mb-3"
                            />
                            <p class="text-sm opacity-50 mb-4">No books yet</p>
                            <button
                                class="px-4 py-2 bg-primary text-white text-sm font-medium rounded-md hover:opacity-90 transition-opacity cursor-pointer"
                                @click="openCreateModal"
                            >
                                Create your first book
                            </button>
                        </div>

                        <div
                            v-else
                            class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"
                        >
                            <div
                                v-for="book in recentBooks"
                                :key="book.id"
                                class="p-4 bg-[var(--section-alt-bg)] border border-[var(--border-color)] rounded-lg cursor-pointer hover:border-primary/30 transition-colors"
                                @click="selectBook(book)"
                                @dblclick="openBookInEditor(book.id)"
                            >
                                <div
                                    class="flex items-start justify-between gap-3 mb-2"
                                >
                                    <h3 class="text-sm font-medium truncate">
                                        {{ book.title }}
                                    </h3>
                                    <span
                                        class="text-[10px] font-medium px-1.5 py-0.5 rounded shrink-0"
                                        :class="
                                            book.status === 'Published'
                                                ? 'bg-primary/10 text-primary'
                                                : 'bg-[var(--border-color)]'
                                        "
                                    >
                                        {{ book.status }}
                                    </span>
                                </div>
                                <p
                                    v-if="book.description"
                                    class="text-xs opacity-50 mb-3 line-clamp-2"
                                >
                                    {{ book.description }}
                                </p>
                                <div class="text-xs opacity-40">
                                    {{ book.page_count }} pages &middot;
                                    {{ formatDate(book.modified_at) }}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Book Detail View -->
                <div v-else class="max-w-4xl mx-auto px-6 py-10">
                    <div class="mb-8">
                        <div class="flex items-center gap-3 mb-2">
                            <h1 class="text-2xl font-semibold">
                                {{ selectedBook.title }}
                            </h1>
                            <span
                                class="text-xs font-medium px-2 py-1 rounded"
                                :class="
                                    selectedBook.status === 'Published'
                                        ? 'bg-primary/10 text-primary'
                                        : 'bg-[var(--border-color)]'
                                "
                            >
                                {{ selectedBook.status }}
                            </span>
                        </div>
                        <p
                            v-if="selectedBook.description"
                            class="text-sm opacity-60 mb-2"
                        >
                            {{ selectedBook.description }}
                        </p>
                        <div class="text-xs opacity-40">
                            {{ selectedBook.page_count }} pages &middot;
                            {{ selectedBook.image_count }} images &middot;
                            {{ formatSize(selectedBook.book_size) }} &middot;
                            Updated {{ formatDate(selectedBook.modified_at) }}
                        </div>
                    </div>

                    <!-- Actions -->
                    <div
                        class="flex flex-wrap gap-2 pb-8 mb-8 border-b border-[var(--border-color)]"
                    >
                        <button
                            class="flex items-center gap-2 px-4 py-2 bg-primary text-white text-sm font-medium rounded-md hover:opacity-90 transition-opacity cursor-pointer"
                            @click="openBookInEditor(selectedBook.id)"
                        >
                            <BaseIcon name="edit" :size="15" />
                            Open in Editor
                        </button>
                        <button
                            class="flex items-center gap-2 px-4 py-2 bg-[var(--section-alt-bg)] border border-[var(--border-color)] text-sm rounded-md hover:bg-[var(--border-color)] transition-colors cursor-pointer"
                            @click="openEditModal(selectedBook)"
                        >
                            <BaseIcon name="settings" :size="15" />
                            Edit Details
                        </button>
                        <button
                            class="flex items-center gap-2 px-4 py-2 bg-[var(--section-alt-bg)] border border-[var(--border-color)] text-sm rounded-md hover:bg-[var(--border-color)] transition-colors cursor-pointer"
                            @click="handleTogglePublish(selectedBook)"
                        >
                            <BaseIcon
                                :name="
                                    selectedBook.status === 'Published'
                                        ? 'eye-off'
                                        : 'eye'
                                "
                                :size="15"
                            />
                            {{
                                selectedBook.status === "Published"
                                    ? "Unpublish"
                                    : "Publish"
                            }}
                        </button>
                        <button
                            v-if="selectedBook.status === 'Published'"
                            class="flex items-center gap-2 px-4 py-2 bg-[var(--section-alt-bg)] border border-[var(--border-color)] text-sm rounded-md hover:bg-[var(--border-color)] transition-colors cursor-pointer"
                            @click="openShareModal(selectedBook)"
                        >
                            <BaseIcon name="share" :size="15" />
                            Share
                        </button>
                        <button
                            class="flex items-center gap-2 px-4 py-2 bg-[var(--section-alt-bg)] border border-[var(--border-color)] text-sm rounded-md hover:bg-[var(--border-color)] transition-colors text-[var(--btn-delete-bg)] cursor-pointer"
                            @click="openDeleteModal(selectedBook)"
                        >
                            <BaseIcon name="trash" :size="15" />
                            Delete
                        </button>
                    </div>

                    <!-- Pages -->
                    <div>
                        <div class="flex items-center justify-between mb-4">
                            <h2 class="text-base font-medium">Pages</h2>
                            <span class="text-xs opacity-40">
                                {{ selectedBook.page_count }} pages
                            </span>
                        </div>

                        <div
                            v-if="!bookPages[selectedBook.id]"
                            class="text-sm opacity-50 py-8 text-center"
                        >
                            Loading pages...
                        </div>

                        <div
                            v-else-if="bookPages[selectedBook.id]?.length === 0"
                            class="text-center py-12 border border-dashed border-[var(--border-color)] rounded-lg"
                        >
                            <p class="text-sm opacity-50 mb-4">
                                This book has no pages yet.
                            </p>
                            <button
                                class="px-4 py-2 bg-primary text-white text-sm font-medium rounded-md hover:opacity-90 transition-opacity cursor-pointer"
                                @click="openBookInEditor(selectedBook.id)"
                            >
                                Start writing
                            </button>
                        </div>

                        <div
                            v-else
                            class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-3"
                        >
                            <div
                                v-for="page in bookPages[selectedBook.id]"
                                :key="page.id"
                                class="aspect-[3/4] p-3 bg-[var(--page-bg)] border border-[var(--border-color)] rounded-md cursor-pointer hover:border-primary/30 transition-colors overflow-hidden"
                                @click="
                                    openPageInEditor(
                                        selectedBook.id,
                                        page.page_number,
                                    )
                                "
                            >
                                <div
                                    class="text-[10px] font-medium opacity-40 mb-2"
                                >
                                    {{ page.page_number }}
                                </div>
                                <div
                                    class="text-[10px] leading-relaxed opacity-50 line-clamp-6"
                                >
                                    {{
                                        getPagePreview(page.content) || "Empty"
                                    }}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </main>

        <!-- Context Menu -->
        <Teleport to="body">
            <Transition
                enter-active-class="transition duration-75 ease-out"
                enter-from-class="opacity-0 scale-95"
                enter-to-class="opacity-100 scale-100"
                leave-active-class="transition duration-50 ease-in"
                leave-from-class="opacity-100 scale-100"
                leave-to-class="opacity-0 scale-95"
            >
                <div
                    v-if="contextMenu.visible"
                    ref="contextMenuRef"
                    class="fixed z-[1000] min-w-[160px] bg-[var(--page-bg)] border border-[var(--border-color)] rounded-md shadow-lg p-1"
                    :style="{
                        left: `${contextMenu.x}px`,
                        top: `${contextMenu.y}px`,
                    }"
                >
                    <template v-if="contextMenu.type === 'book'">
                        <button
                            class="w-full flex items-center gap-2.5 px-2.5 py-2 text-sm rounded hover:bg-[var(--border-color)] transition-colors cursor-pointer"
                            @click="handleContextAction('open')"
                        >
                            <BaseIcon name="external-link" :size="14" />
                            Open in Editor
                        </button>
                        <button
                            class="w-full flex items-center gap-2.5 px-2.5 py-2 text-sm rounded hover:bg-[var(--border-color)] transition-colors cursor-pointer"
                            @click="handleContextAction('edit')"
                        >
                            <BaseIcon name="edit" :size="14" />
                            Edit Details
                        </button>
                        <button
                            class="w-full flex items-center gap-2.5 px-2.5 py-2 text-sm rounded hover:bg-[var(--border-color)] transition-colors cursor-pointer"
                            @click="handleContextAction('publish')"
                        >
                            <BaseIcon
                                :name="
                                    contextMenuBook?.status === 'Published'
                                        ? 'eye-off'
                                        : 'eye'
                                "
                                :size="14"
                            />
                            {{
                                contextMenuBook?.status === "Published"
                                    ? "Unpublish"
                                    : "Publish"
                            }}
                        </button>
                        <button
                            v-if="contextMenuBook?.status === 'Published'"
                            class="w-full flex items-center gap-2.5 px-2.5 py-2 text-sm rounded hover:bg-[var(--border-color)] transition-colors cursor-pointer"
                            @click="handleContextAction('share')"
                        >
                            <BaseIcon name="share" :size="14" />
                            Share
                        </button>
                        <div class="h-px bg-[var(--border-color)] my-1" />
                        <button
                            class="w-full flex items-center gap-2.5 px-2.5 py-2 text-sm rounded hover:bg-[var(--border-color)] transition-colors text-[var(--btn-delete-bg)] cursor-pointer"
                            @click="handleContextAction('delete')"
                        >
                            <BaseIcon name="trash" :size="14" />
                            Delete
                        </button>
                    </template>
                    <template v-else-if="contextMenu.type === 'page'">
                        <button
                            class="w-full flex items-center gap-2.5 px-2.5 py-2 text-sm rounded hover:bg-[var(--border-color)] transition-colors cursor-pointer"
                            @click="handleContextAction('openPage')"
                        >
                            <BaseIcon name="external-link" :size="14" />
                            Open Page
                        </button>
                    </template>
                </div>
            </Transition>
        </Teleport>

        <!-- Create/Edit Book Modal -->
        <BaseModal
            :visible="bookModalVisible"
            :title="editingBook ? 'Edit Book' : 'Create New Book'"
            size="sm"
            @close="closeBookModal"
        >
            <form @submit.prevent="handleBookSubmit">
                <div class="mb-4">
                    <label class="block text-sm font-medium mb-1.5"
                        >Title</label
                    >
                    <input
                        v-model="bookForm.title"
                        type="text"
                        required
                        placeholder="Book title"
                        class="w-full px-3 py-2 text-sm bg-[var(--bg-color)] border border-[var(--border-color)] rounded-md outline-none transition-colors focus:border-primary"
                    />
                </div>
                <div class="mb-4">
                    <label class="block text-sm font-medium mb-1.5"
                        >Description</label
                    >
                    <textarea
                        v-model="bookForm.description"
                        rows="3"
                        placeholder="Optional description"
                        class="w-full px-3 py-2 text-sm bg-[var(--bg-color)] border border-[var(--border-color)] rounded-md outline-none transition-colors focus:border-primary resize-none"
                    />
                </div>
                <div class="mb-4">
                    <label class="block text-sm font-medium mb-1.5">Year</label>
                    <input
                        v-model.number="bookForm.year"
                        type="number"
                        :min="1900"
                        :max="new Date().getFullYear()"
                        placeholder="Publication year"
                        class="w-full px-3 py-2 text-sm bg-[var(--bg-color)] border border-[var(--border-color)] rounded-md outline-none transition-colors focus:border-primary"
                    />
                </div>
            </form>
            <template #footer>
                <button
                    class="px-4 py-2 text-sm bg-transparent border border-[var(--border-color)] rounded-md hover:bg-[var(--section-alt-bg)] transition-colors cursor-pointer"
                    @click="closeBookModal"
                >
                    Cancel
                </button>
                <button
                    class="px-4 py-2 text-sm font-medium text-white bg-primary rounded-md hover:opacity-90 transition-opacity disabled:opacity-50 cursor-pointer"
                    :disabled="bookSubmitting || !bookForm.title.trim()"
                    @click="handleBookSubmit"
                >
                    {{
                        bookSubmitting
                            ? "Saving..."
                            : editingBook
                              ? "Update"
                              : "Create"
                    }}
                </button>
            </template>
        </BaseModal>

        <!-- Delete Confirmation Modal -->
        <BaseModal
            :visible="deleteModalVisible"
            title="Delete Book"
            size="sm"
            @close="closeDeleteModal"
        >
            <p class="text-sm">
                Are you sure you want to delete
                <strong>{{ deletingBook?.title }}</strong
                >? This action cannot be undone.
            </p>
            <template #footer>
                <button
                    class="px-4 py-2 text-sm bg-transparent border border-[var(--border-color)] rounded-md hover:bg-[var(--section-alt-bg)] transition-colors cursor-pointer"
                    @click="closeDeleteModal"
                >
                    Cancel
                </button>
                <button
                    class="px-4 py-2 text-sm font-medium text-white bg-[var(--btn-delete-bg)] rounded-md hover:opacity-90 transition-opacity disabled:opacity-50 cursor-pointer"
                    :disabled="deleteSubmitting"
                    @click="handleDeleteConfirm"
                >
                    {{ deleteSubmitting ? "Deleting..." : "Delete" }}
                </button>
            </template>
        </BaseModal>

        <!-- Share Book Modal -->
        <BaseModal
            :visible="shareModalVisible"
            title="Share Book"
            size="sm"
            @close="closeShareModal"
        >
            <div class="space-y-4">
                <div
                    v-if="shareLoading"
                    class="py-8 text-center text-sm opacity-60"
                >
                    Generating share link...
                </div>

                <div
                    v-else-if="shareError"
                    class="py-6 text-center text-sm text-[var(--btn-delete-bg)]"
                >
                    {{ shareError }}
                </div>

                <template v-else-if="shareLink">
                    <p class="text-sm opacity-60">
                        Anyone with the link can view a snapshot of
                        <strong>{{ sharingBook?.title }}</strong
                        >.
                    </p>

                    <div class="flex gap-2">
                        <button
                            class="flex-1 flex items-center justify-center gap-2 px-3 py-2.5 text-sm bg-[var(--bg-color)] border border-[var(--border-color)] rounded-md hover:border-primary hover:text-primary transition-colors cursor-pointer"
                            @click="shareVia('whatsapp')"
                        >
                            WhatsApp
                        </button>
                        <button
                            class="flex-1 flex items-center justify-center gap-2 px-3 py-2.5 text-sm bg-[var(--bg-color)] border border-[var(--border-color)] rounded-md hover:border-primary hover:text-primary transition-colors cursor-pointer"
                            @click="shareVia('facebook')"
                        >
                            Facebook
                        </button>
                        <button
                            class="flex-1 flex items-center justify-center gap-2 px-3 py-2.5 text-sm bg-[var(--bg-color)] border border-[var(--border-color)] rounded-md hover:border-primary hover:text-primary transition-colors cursor-pointer"
                            @click="shareVia('telegram')"
                        >
                            Telegram
                        </button>
                    </div>

                    <div class="pt-4 border-t border-[var(--border-color)]">
                        <label class="block text-xs font-medium opacity-50 mb-2"
                            >Book Link</label
                        >
                        <div class="flex gap-2">
                            <input
                                type="text"
                                readonly
                                :value="shareLink"
                                class="flex-1 px-3 py-2 text-xs bg-[var(--bg-color)] border border-[var(--border-color)] rounded-md"
                            />
                            <button
                                class="px-4 py-2 text-xs font-medium text-white bg-primary rounded-md hover:opacity-90 transition-opacity cursor-pointer"
                                @click="copyShareLink"
                            >
                                {{ linkCopied ? "Copied!" : "Copy" }}
                            </button>
                        </div>
                    </div>
                </template>
            </div>
        </BaseModal>

        <!-- Settings Dialog -->
        <SettingsDialog v-model:visible="showSettings" />
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from "vue";
import { useRouter } from "vue-router";
import { useTheme } from "@/composables/useTheme";
import { useClickOutside } from "@/composables/useClickOutside";
import { isAuthenticated, logout } from "@/api/auth";
import { getProfile } from "@/api/profile";
import {
    getBooks,
    getBook,
    createBook,
    updateBook,
    deleteBook as deleteBookApi,
    togglePublishBook,
    type BookPage,
} from "@/api/books";
import { shareBook as shareBookApi } from "@/api/sharing";
import { logger } from "@/utils/logger";
import type { BookSummary } from "@/types";
import BaseIcon from "@/components/ui/BaseIcon.vue";
import BaseModal from "@/components/ui/BaseModal.vue";
import NotificationDropdown from "@/components/NotificationDropdown.vue";
import SettingsDialog from "@/components/settings/SettingsDialog.vue";

interface UserProfile {
    id: number;
    email: string;
    full_name: string;
    first_name: string;
    last_name: string;
}

const router = useRouter();
const { isDarkTheme, toggleTheme } = useTheme();

// User state
const user = ref<UserProfile | null>(null);
const initials = computed(() => {
    const u = user.value;
    if (!u) return "?";
    const first = u.first_name?.[0] || "";
    const last = u.last_name?.[0] || "";
    return (first + last).toUpperCase() || u.email?.[0]?.toUpperCase() || "?";
});

// Sidebar state
const sidebarCollapsed = ref(false);
const sidebarWidth = ref(260);
const isResizing = ref(false);
const userDropdownOpen = ref(false);
const userDropdownRef = ref<HTMLElement | null>(null);
const showSettings = ref(false);
const searchQuery = ref("");

// Books state
const books = ref<BookSummary[]>([]);
const loading = ref(true);
const expandedBooks = ref<Set<number>>(new Set());
const bookPages = ref<Record<number, BookPage[]>>({});
const selectedBookId = ref<number | null>(null);
const selectedPageId = ref<number | null>(null);

// Computed
const totalPages = computed(() =>
    books.value.reduce((sum, b) => sum + b.page_count, 0),
);
const totalImages = computed(() =>
    books.value.reduce((sum, b) => sum + b.image_count, 0),
);
const publishedCount = computed(
    () => books.value.filter((b) => b.status === "Published").length,
);
const selectedBook = computed(() =>
    books.value.find((b) => b.id === selectedBookId.value),
);
const recentBooks = computed(() =>
    [...books.value]
        .sort(
            (a, b) =>
                new Date(b.modified_at).getTime() -
                new Date(a.modified_at).getTime(),
        )
        .slice(0, 6),
);
const filteredBooks = computed(() => {
    if (!searchQuery.value) return books.value;
    const q = searchQuery.value.toLowerCase();
    return books.value.filter(
        (b) =>
            b.title.toLowerCase().includes(q) ||
            b.description?.toLowerCase().includes(q),
    );
});

// Context menu
const contextMenu = ref<{
    visible: boolean;
    x: number;
    y: number;
    type: "book" | "page";
    data: BookSummary | { book: BookSummary; page: BookPage } | null;
}>({
    visible: false,
    x: 0,
    y: 0,
    type: "book",
    data: null,
});
const contextMenuRef = ref<HTMLElement | null>(null);

const contextMenuBook = computed((): BookSummary | null => {
    if (!contextMenu.value.data) return null;
    if (contextMenu.value.type === "book") {
        return contextMenu.value.data as BookSummary;
    }
    return (contextMenu.value.data as { book: BookSummary; page: BookPage })
        .book;
});

// Sidebar resize
function startResize(e: MouseEvent) {
    isResizing.value = true;
    document.addEventListener("mousemove", handleResize);
    document.addEventListener("mouseup", stopResize);
    e.preventDefault();
}

function handleResize(e: MouseEvent) {
    if (!isResizing.value) return;
    sidebarWidth.value = Math.min(Math.max(e.clientX, 200), 400);
}

function stopResize() {
    isResizing.value = false;
    document.removeEventListener("mousemove", handleResize);
    document.removeEventListener("mouseup", stopResize);
}

// Book tree
async function toggleBookExpanded(bookId: number) {
    if (expandedBooks.value.has(bookId)) {
        expandedBooks.value.delete(bookId);
    } else {
        expandedBooks.value.add(bookId);
        if (!bookPages.value[bookId]) {
            await loadBookPages(bookId);
        }
    }
    expandedBooks.value = new Set(expandedBooks.value);
}

async function loadBookPages(bookId: number) {
    try {
        const bookDetail = await getBook(bookId);
        if (bookDetail) {
            bookPages.value[bookId] = bookDetail.pages;
        }
    } catch (err) {
        logger.error("Failed to load book pages:", err);
        bookPages.value[bookId] = [];
    }
}

function selectBook(book: BookSummary) {
    selectedBookId.value = book.id;
    selectedPageId.value = null;
    if (!bookPages.value[book.id]) {
        loadBookPages(book.id);
    }
}

function selectPage(book: BookSummary, page: BookPage) {
    selectedBookId.value = book.id;
    selectedPageId.value = page.id;
}

function openBookInEditor(bookId: number) {
    router.push({ path: "/edit", query: { book: String(bookId) } });
}

function openPageInEditor(bookId: number, pageNumber: number) {
    router.push({
        path: "/edit",
        query: { book: String(bookId), page: String(pageNumber) },
    });
}

// Context menu
function openContextMenu(
    e: MouseEvent,
    type: "book" | "page",
    data: BookSummary | { book: BookSummary; page: BookPage },
) {
    contextMenu.value = {
        visible: true,
        x: e.clientX,
        y: e.clientY,
        type,
        data,
    };
}

function closeContextMenu() {
    contextMenu.value.visible = false;
}

function handleContextAction(
    action: "open" | "edit" | "publish" | "share" | "delete" | "openPage",
) {
    const { type, data } = contextMenu.value;
    closeContextMenu();

    if (type === "book" && data) {
        const book = data as BookSummary;
        switch (action) {
            case "open":
                openBookInEditor(book.id);
                break;
            case "edit":
                openEditModal(book);
                break;
            case "publish":
                handleTogglePublish(book);
                break;
            case "share":
                openShareModal(book);
                break;
            case "delete":
                openDeleteModal(book);
                break;
        }
    } else if (type === "page" && data) {
        const { book, page } = data as { book: BookSummary; page: BookPage };
        if (action === "openPage") {
            openPageInEditor(book.id, page.page_number);
        }
    }
}

// Create/Edit Book Modal
const bookModalVisible = ref(false);
const editingBook = ref<BookSummary | null>(null);
const bookSubmitting = ref(false);
const bookForm = ref({
    title: "",
    description: "",
    year: new Date().getFullYear(),
});

function openCreateModal() {
    editingBook.value = null;
    bookForm.value = {
        title: "",
        description: "",
        year: new Date().getFullYear(),
    };
    bookModalVisible.value = true;
}

function openEditModal(book: BookSummary) {
    editingBook.value = book;
    bookForm.value = {
        title: book.title,
        description: book.description ?? "",
        year: book.year,
    };
    bookModalVisible.value = true;
}

function closeBookModal() {
    bookModalVisible.value = false;
    editingBook.value = null;
}

async function handleBookSubmit() {
    if (!bookForm.value.title.trim()) return;
    bookSubmitting.value = true;
    try {
        if (editingBook.value) {
            await updateBook(editingBook.value.id, {
                title: bookForm.value.title,
                description: bookForm.value.description,
                year: bookForm.value.year,
            });
        } else {
            await createBook({
                title: bookForm.value.title,
                description: bookForm.value.description,
                year: bookForm.value.year,
            });
        }
        closeBookModal();
        books.value = await getBooks();
    } finally {
        bookSubmitting.value = false;
    }
}

// Delete Book Modal
const deleteModalVisible = ref(false);
const deletingBook = ref<BookSummary | null>(null);
const deleteSubmitting = ref(false);

function openDeleteModal(book: BookSummary) {
    deletingBook.value = book;
    deleteModalVisible.value = true;
}

function closeDeleteModal() {
    deleteModalVisible.value = false;
    deletingBook.value = null;
}

async function handleDeleteConfirm() {
    if (!deletingBook.value) return;
    deleteSubmitting.value = true;
    try {
        await deleteBookApi(deletingBook.value.id);
        if (selectedBookId.value === deletingBook.value.id) {
            selectedBookId.value = null;
        }
        closeDeleteModal();
        books.value = await getBooks();
    } finally {
        deleteSubmitting.value = false;
    }
}

// Share Book Modal
const shareModalVisible = ref(false);
const sharingBook = ref<BookSummary | null>(null);
const shareLoading = ref(false);
const shareError = ref("");
const shareLink = ref("");
const linkCopied = ref(false);

const shareMessage =
    "This book was written on Doccoon editor. View it by clicking on the link below!";

async function handleTogglePublish(book: BookSummary) {
    try {
        const result = await togglePublishBook(book.id);
        if (result) {
            book.status = result.status;
            const idx = books.value.findIndex((b) => b.id === book.id);
            if (idx !== -1 && books.value[idx]) {
                books.value[idx].status = result.status;
            }
        }
    } catch (err) {
        logger.error("Publish toggle error:", err);
    }
}

async function openShareModal(book: BookSummary) {
    sharingBook.value = book;
    shareLink.value = "";
    shareError.value = "";
    shareLoading.value = true;
    shareModalVisible.value = true;

    try {
        const result = await shareBookApi(book.id);
        if (result?.share_token) {
            shareLink.value = `${window.location.origin}/shared/book/${result.share_token}`;
        } else {
            shareError.value = "Failed to generate share link.";
        }
    } catch (err: unknown) {
        const error = err as { message?: string };
        logger.error("Share book error:", error);
        shareError.value =
            error.message || "Failed to share book. Please try again.";
    } finally {
        shareLoading.value = false;
    }
}

function closeShareModal() {
    shareModalVisible.value = false;
    sharingBook.value = null;
    shareLink.value = "";
    shareError.value = "";
    linkCopied.value = false;
}

function shareVia(platform: "whatsapp" | "facebook" | "telegram") {
    if (!shareLink.value) return;
    const text = `${shareMessage}\n${shareLink.value}`;
    let url = "";

    switch (platform) {
        case "whatsapp":
            url = `https://wa.me/?text=${encodeURIComponent(text)}`;
            break;
        case "facebook":
            url = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(shareLink.value)}&quote=${encodeURIComponent(shareMessage)}`;
            break;
        case "telegram":
            url = `https://t.me/share/url?url=${encodeURIComponent(shareLink.value)}&text=${encodeURIComponent(shareMessage)}`;
            break;
    }

    window.open(url, "_blank", "noopener,noreferrer");
}

async function copyShareLink() {
    if (!shareLink.value) return;
    try {
        await navigator.clipboard.writeText(shareLink.value);
        linkCopied.value = true;
        setTimeout(() => {
            linkCopied.value = false;
        }, 2000);
    } catch (err) {
        logger.error("Failed to copy link:", err);
    }
}

// Helpers
function formatDate(dateStr: string): string {
    const date = new Date(dateStr);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

    if (diffDays === 0) return "today";
    if (diffDays === 1) return "yesterday";
    if (diffDays < 30) return `${diffDays}d ago`;

    return date.toLocaleDateString("en-US", {
        month: "short",
        day: "numeric",
        year: date.getFullYear() !== now.getFullYear() ? "numeric" : undefined,
    });
}

function formatSize(bytes: number): string {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

function getPagePreview(content: string): string {
    if (!content) return "";
    const plain = content
        .replace(/[#*_`~\[\]()]/g, "")
        .replace(/\n+/g, " ")
        .trim();
    return plain.length > 100 ? plain.slice(0, 100) + "..." : plain;
}

function openSettings() {
    userDropdownOpen.value = false;
    showSettings.value = true;
}

function handleLogout() {
    userDropdownOpen.value = false;
    logout();
}

// Click outside
useClickOutside(userDropdownRef, () => {
    userDropdownOpen.value = false;
});

useClickOutside(contextMenuRef, () => {
    closeContextMenu();
});

// Keyboard
function handleKeydown(e: KeyboardEvent) {
    if (e.key === "Escape") {
        if (contextMenu.value.visible) closeContextMenu();
        if (userDropdownOpen.value) userDropdownOpen.value = false;
    }
}

// Lifecycle
onMounted(async () => {
    if (!isAuthenticated()) {
        router.push("/login");
        return;
    }

    document.addEventListener("keydown", handleKeydown);

    try {
        const [profile, bookList] = await Promise.all([
            getProfile(),
            getBooks(),
        ]);
        user.value = profile;
        books.value = bookList;
    } finally {
        loading.value = false;
    }
});

onUnmounted(() => {
    document.removeEventListener("keydown", handleKeydown);
    document.removeEventListener("mousemove", handleResize);
    document.removeEventListener("mouseup", stopResize);
});

watch(isResizing, (resizing) => {
    document.body.style.cursor = resizing ? "col-resize" : "";
    document.body.style.userSelect = resizing ? "none" : "";
});
</script>
